import threading
import time
import random

# Constants
NUM_ROADS = 4
ROAD_NAMES = ['A', 'B', 'C', 'D']

# Synchronization Primitives
road_semaphores = [threading.Semaphore(1) for _ in range(NUM_ROADS)]
traffic_data_lock = threading.Lock()

# Global State
traffic = [0] * NUM_ROADS
emergency_flag = False
current_green = -1

def traffic_update():
    """Simulates real-time traffic density updates"""
    global traffic
    while True:
        with traffic_data_lock:
            print("\n🔄 Updating Traffic Data...")
            for i in range(NUM_ROADS):
                new_vehicles = random.randint(0, 4)
                traffic[i] += new_vehicles
                print(f"🚗 Road {ROAD_NAMES[i]}: +{new_vehicles} new vehicles (Total: {traffic[i]})")
        time.sleep(3)

def emergency_vehicle():
    """Handles priority emergency vehicle movement"""
    global emergency_flag, current_green, traffic
    
    with traffic_data_lock:
        emergency_flag = True
        start_road = random.randint(0, NUM_ROADS - 1)
        end_road = random.randint(0, NUM_ROADS - 1)
        while end_road == start_road:
            end_road = random.randint(0, NUM_ROADS - 1)

        print(f"\n🚨 EMERGENCY: Vehicle from Road {ROAD_NAMES[start_road]} to {ROAD_NAMES[end_road]}!")
        
        # Clear the road
        traffic[start_road] = 0
        current_green = start_road
        print(f"✅ Emergency route cleared on Road {ROAD_NAMES[start_road]}.")
        
        emergency_flag = False

def traffic_signal():
    """Main control logic for switching lights"""
    global current_green, traffic
    while True:
        with traffic_data_lock:
            if emergency_flag:
                continue
            
            max_traffic_road = traffic.index(max(traffic))
            current_green = max_traffic_road
            
            print(f"\n✅ Road {ROAD_NAMES[current_green]}: GREEN | ❌ Others: RED (Traffic: {traffic[current_green]})")
        
        time.sleep(1)
        
        with traffic_data_lock:
            if traffic[current_green] > 0:
                print(f"🚗 Clearing traffic on Road {ROAD_NAMES[current_green]}...")
                traffic[current_green] = 0
                print(f"✅ Road {ROAD_NAMES[current_green]} cleared.")
        
        time.sleep(4)

def simulate_car(road_index):
    """Simulates an individual car attempting to pass"""
    global traffic
    # Using the semaphore to control access to the road
    with road_semaphores[road_index]:
        with traffic_data_lock:
            if traffic[road_index] > 0 and road_index == current_green:
                traffic[road_index] -= 1
                print(f"🚗 Car successfully passed Road {ROAD_NAMES[road_index]} (Remaining: {traffic[road_index]})")

def main():
    print("🚦 Starting Smart Traffic Management System (Python Version) 🚦")
    threading.Thread(target=traffic_update, daemon=True).start()
    threading.Thread(target=traffic_signal, daemon=True).start()

    try:
        while True:
            # Randomly spawn cars
            road_choice = random.randint(0, NUM_ROADS - 1)
            threading.Thread(target=simulate_car, args=(road_choice,)).start()
            
            # 20% chance to spawn an emergency vehicle
            if random.random() < 0.2:
                threading.Thread(target=emergency_vehicle).start()
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 System shutting down...")

if __name__ == "__main__":
    main()
