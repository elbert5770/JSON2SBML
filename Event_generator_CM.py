def generate_events(n, start_time_years=70, interval_weeks=2):
    """
    Generate n event lines based on the template.
    
    Args:
        n (int): Number of events to generate
        base_time_years (int): Base time in years (default: 70)
        interval_weeks (int): Interval between events in weeks (default: 2)
    
    Returns:
        list: List of generated event strings
    """
    events = []
    
    for i in range(1, n + 1):
        # Calculate the time offset: base_time + (i-1) * interval_weeks * 7 days * 24 hours
        time_offset = (i - 1) * interval_weeks * 7 * 24
        
        # Generate the event line
        event_line = f"E{i}: at (time >= {start_time_years}*365*24 + {interval_weeks}*7*24*{i-1}): Antibody_Plasma = Antibody_Plasma + Antibody_IV_Dose"
        events.append(event_line)
    
    return events

def main():
    # Example usage
    start_time_years = 70
    n_events = 39  # Change this to generate more or fewer events
    interval_weeks = 2 # dose interval in weeks
    print("Generated Events:")
    print("=" * 50)
    
    events = generate_events(n_events, start_time_years, interval_weeks)
    
    for event in events:
        print(event)
    
    print("\n" + "=" * 50)
    print(f"Generated {n_events} events")
    
    # Option to save to file
    
    filename = "generated_events.txt"
    with open(filename, 'w') as f:
        for event in events:
            f.write(event + '\n')
    print(f"Events saved to {filename}")

if __name__ == "__main__":
    main()
