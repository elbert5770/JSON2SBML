# libRoadRunner + Enzyme Integration Guide

## Overview

This guide details how to integrate Enzyme automatic differentiation into libRoadRunner's existing LLVM-based compilation pipeline for systems biology models.

## Current libRoadRunner Architecture

```
SBML Model → AST → IL (Intermediate Language) → LLVM IR → Machine Code
                                                    ↑
                                            Optimization Passes
```

## Integration Points

### 1. LLVM Module Integration

libRoadRunner generates LLVM modules containing functions for:
- Rate equations
- Species concentrations
- Parameter updates
- Jacobian computations (manual)

**Integration Strategy:**
```cpp
// In libRoadRunner's LLVMExecutableModel class
#include "enzyme/Enzyme.h"

class LLVMExecutableModel {
private:
    llvm::Module* module;
    llvm::ExecutionEngine* engine;
    
public:
    // Add Enzyme differentiation
    llvm::Function* generateDerivative(llvm::Function* original, 
                                     const std::vector<int>& diffArgs) {
        // Create Enzyme configuration
        EnzymeLogic logic;
        
        // Generate derivative function
        return logic.CreateForwardDiff(original, diffArgs, module);
    }
};
```

### 2. Compilation Pipeline Modification

**Current Pipeline:**
```cpp
// Existing libRoadRunner compilation
void LLVMModelGenerator::generateFunction() {
    // 1. Parse SBML to AST
    // 2. Convert AST to IL
    // 3. Generate LLVM IR
    // 4. Optimize IR
    // 5. JIT compile
}
```

**Modified Pipeline with Enzyme:**
```cpp
void LLVMModelGenerator::generateFunction() {
    // 1-3. Existing steps...
    
    // 4. Generate derivative functions with Enzyme
    generateAutodiffFunctions();
    
    // 5. Optimize IR (including new derivative functions)
    // 6. JIT compile
}

void LLVMModelGenerator::generateAutodiffFunctions() {
    // For each rate equation function
    for (auto& func : rateFunctions) {
        // Generate forward-mode derivatives
        auto forwardDiff = enzyme->CreateForwardDiff(func, paramIndices);
        
        // Generate reverse-mode derivatives  
        auto reverseDiff = enzyme->CreateReverseDiff(func, paramIndices);
        
        // Add to module
        module->getFunctionList().push_back(forwardDiff);
        module->getFunctionList().push_back(reverseDiff);
    }
}
```

### 3. Memory Management Integration

Enzyme requires careful memory management for gradient computations:

```cpp
class EnzymeMemoryManager {
private:
    std::vector<double*> gradientBuffers;
    
public:
    double* allocateGradientBuffer(size_t size) {
        auto buffer = new double[size]();
        gradientBuffers.push_back(buffer);
        return buffer;
    }
    
    void cleanup() {
        for (auto* buffer : gradientBuffers) {
            delete[] buffer;
        }
        gradientBuffers.clear();
    }
};
```

## Technical Implementation Details

### 1. Function Signature Handling

libRoadRunner functions typically have signatures like:
```cpp
// Original rate function
double rateFunction(double* species, double* parameters, double time);

// Enzyme-generated derivative
void rateFunction_fwd(double* species, double* species_dot,
                      double* parameters, double* parameters_dot,
                      double time, double* result, double* result_dot);
```

### 2. Integration with Existing Jacobian Computation

Replace manual Jacobian generation:
```cpp
// Old approach - manual symbolic differentiation
void generateJacobian() {
    // Manual derivative computation
    for (int i = 0; i < numSpecies; ++i) {
        for (int j = 0; j < numSpecies; ++j) {
            jacobian[i][j] = computeManualDerivative(i, j);
        }
    }
}

// New approach - Enzyme automatic differentiation
void generateJacobianWithEnzyme() {
    // Use Enzyme to compute Jacobian
    auto jacobianFunc = enzyme->CreateJacobian(rateFunction, speciesIndices);
    
    // Call generated function
    jacobianFunc(species, parameters, time, jacobian);
}
```

### 3. Build System Integration

**CMake Configuration:**
```cmake
# Find Enzyme
find_package(Enzyme REQUIRED)

# Add Enzyme to libRoadRunner
target_link_libraries(roadrunner 
    PRIVATE 
    Enzyme::Enzyme
    ${LLVM_LIBRARIES}
)

# Ensure compatible LLVM versions
set(LLVM_MIN_VERSION "14.0")
```

**Header Integration:**
```cpp
// In LLVMIncludes.h
#include "enzyme/Enzyme.h"
#include "llvm/Transforms/Utils/Cloning.h"
#include "llvm/IR/Verifier.h"
```

## API Extensions

### 1. C++ API Extensions

```cpp
class RoadRunner {
public:
    // New autodiff methods
    void enableAutomaticDifferentiation(bool enable = true);
    
    // Get parameter sensitivities
    std::vector<double> getParameterSensitivities(const std::string& species);
    
    // Get full sensitivity matrix
    ls::Matrix<double> getSensitivityMatrix();
    
    // Gradient-based parameter estimation
    void fitParameters(const std::vector<double>& targetData, 
                      const std::vector<std::string>& parameters);
};
```

### 2. Python API Extensions

```python
# In roadrunner.py
class RoadRunner:
    def enable_autodiff(self, enable=True):
        """Enable automatic differentiation"""
        pass
        
    def get_parameter_sensitivities(self, species_name):
        """Get sensitivities of species to all parameters"""
        pass
        
    def get_sensitivity_matrix(self):
        """Get full sensitivity matrix"""
        pass
```

## Performance Considerations

### 1. Compilation Time
- Enzyme adds compilation overhead
- Consider caching compiled derivative functions
- Use lazy evaluation for derivatives

### 2. Memory Usage
- Gradient computations require additional memory
- Implement memory pooling for gradient buffers
- Use forward-mode for few parameters, reverse-mode for many

### 3. Numerical Stability
- Enzyme preserves numerical properties better than finite differences
- Consider using mixed-mode differentiation for complex models

## Testing Strategy

### 1. Unit Tests
```cpp
TEST(EnzymeIntegration, BasicDerivative) {
    // Load simple SBML model
    RoadRunner r("simple_model.xml");
    r.enableAutomaticDifferentiation();
    
    // Test against known analytical derivatives
    auto sensitivity = r.getParameterSensitivities("S1");
    EXPECT_NEAR(sensitivity[0], expected_value, 1e-10);
}
```

### 2. Regression Tests
- Compare Enzyme results with existing manual derivatives
- Verify performance doesn't degrade significantly
- Test with large systems biology models

## Migration Path

### Phase 1: Core Integration
1. Add Enzyme dependency to build system
2. Implement basic forward-mode differentiation
3. Test with simple models

### Phase 2: Advanced Features
1. Add reverse-mode differentiation
2. Implement sensitivity analysis APIs
3. Optimize performance

### Phase 3: Full Integration
1. Replace manual Jacobian computation
2. Add gradient-based optimization
3. Comprehensive testing with real models

## Common Pitfalls and Solutions

### 1. LLVM Version Compatibility
- Ensure Enzyme and libRoadRunner use compatible LLVM versions
- Test with multiple LLVM versions in CI

### 2. Function Calling Conventions
- Enzyme may change function signatures
- Carefully handle function pointer updates

### 3. Memory Layout
- Ensure gradient buffers have correct memory layout
- Handle structure-of-arrays vs array-of-structures differences

## Example Usage

```cpp
// Load SBML model
RoadRunner r("model.xml");
r.enableAutomaticDifferentiation();

// Run sensitivity analysis
auto result = r.simulate(0, 10, 100);
auto sensitivity = r.getSensitivityMatrix();

// Use gradients for parameter fitting
std::vector<double> targetData = loadExperimentalData();
r.fitParameters(targetData, {"k1", "k2", "k3"});
```

This integration would make libRoadRunner one of the most powerful systems biology simulation engines, combining high-performance LLVM compilation with state-of-the-art automatic differentiation capabilities.