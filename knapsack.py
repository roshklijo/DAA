
def optimize_appliances(appliances, capacity):
    """
    Solve the 0/1 Knapsack problem using Dynamic Programming.

    Each appliance has:
        name     - Appliance name
        power_w  - Power consumption in watts (weight)
        priority - Importance score (value)

    Returns the DP table, selected appliances and total values.
    """

    # Validate capacity
    if not isinstance(capacity, int) or isinstance(capacity, bool):
        raise ValueError("Capacity must be an integer.")

    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")

    # Validate appliances
    for appliance in appliances:
        name = appliance.get("name")
        power = appliance.get("power_w")
        priority = appliance.get("priority")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Every appliance must have a name.")

        if not isinstance(power, int) or isinstance(power, bool) or power <= 0:
            raise ValueError("Appliance power must be a positive integer.")

        if not isinstance(priority, int) or isinstance(priority, bool) or priority <= 0:
            raise ValueError("Appliance priority must be a positive integer.")

    n = len(appliances)

    # Create a DP table filled with zeros
    dp = [[0 for _ in range(capacity + 1)]
          for _ in range(n + 1)]

    # Build the DP table
    for i in range(1, n + 1):

        power = appliances[i - 1]["power_w"]
        priority = appliances[i - 1]["priority"]

        for w in range(capacity + 1):

            # Option 1: Do not select the appliance
            dp[i][w] = dp[i - 1][w]

            # Option 2: Select the appliance if it fits
            if power <= w:
                selected_value = priority + dp[i - 1][w - power]

                dp[i][w] = max(
                    dp[i][w],
                    selected_value
                )

    # Reconstruct the selected appliances
    selected = []
    remaining_capacity = capacity

    for i in range(n, 0, -1):

        if dp[i][remaining_capacity] != dp[i - 1][remaining_capacity]:

            appliance = appliances[i - 1]
            selected.append(appliance)

            remaining_capacity -= appliance["power_w"]

    selected.reverse()

    # Calculate final results
    total_power = sum(item["power_w"] for item in selected)
    total_priority = sum(item["priority"] for item in selected)

    return {
        "selected": selected,
        "total_power": total_power,
        "total_priority": total_priority,
        "remaining_capacity": capacity - total_power,
        "dp_table": dp
    }
