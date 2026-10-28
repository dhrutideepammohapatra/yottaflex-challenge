import csv
import os
import random
from datetime import datetime, timedelta

# Step 3 Parameter & Seed Setup for Reproducibility
SEED = 20261022
random.seed(SEED)

# Scale Parameters (Tunable: Defaulting to a lighter fast mode for immediate local testing)
SCALE_FACTOR = 0.05  # Change to 1.0 for full production baseline volume
NUM_LEARNERS = int(20000 * SCALE_FACTOR)
NUM_COURSES = int(500 * SCALE_FACTOR)
NUM_ENROLLMENTS = int(100000 * SCALE_FACTOR)
NUM_EVENTS = int(2000000 * SCALE_FACTOR)

print(f"Starting data generation with Seed: {SEED} (Scale Factor: {SCALE_FACTOR})...")

# -------------------------------------------------------------
# STEP 1 & 2: MASTER DATA GENERATION
# -------------------------------------------------------------

# 1. Learners
learners = []
for i in range(1, NUM_LEARNERS + 1):
    learners.append({
        "learner_id": f"LRN-{i:06d}",
        "name": f"Learner {i}",
        "email": f"learner{i}@example.com",
        "cohort": f"COHORT-{(i % 5) + 1}"
    })

# 2. Courses & Content Items
courses = []
content_items = []
for i in range(1, NUM_COURSES + 1):
    course_id = f"CRS-{i:06d}"
    courses.append({
        "course_id": course_id,
        "title": f"Course Fundamentals {i}",
        "category": random.choice(["AI", "Data Engineering", "Cloud", "Business Analysis"])
    })
    # Create 3 Content items per course hierarchy
    for c in range(1, 4):
        content_items.append({
            "content_id": f"CNT-{course_id}-{c:02d}",
            "course_id": course_id,
            "type": random.choice(["Video", "Reading", "Quiz"])
        })

# 3. Enrollments
enrollments = []
enrolled_pairs = set()
for i in range(1, NUM_ENROLLMENTS + 1):
    lrn = random.choice(learners)["learner_id"]
    crs = random.choice(courses)["course_id"]
    pair = (lrn, crs)
    
    if pair not in enrolled_pairs:
        enrolled_pairs.add(pair)
        enrollments.append({
            "enrollment_id": f"ENR-{lrn}-{crs}",
            "learner_id": lrn,
            "course_id": crs,
            "enrollment_date": (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d %H:%M:%S")
        })

# -------------------------------------------------------------
# STEP 3 & 5: TRANSACTIONS, EVENTS & ANOMALY INJECTION
# -------------------------------------------------------------
events = []
ground_truth = []

event_types = ["LOGIN", "VIEW_CONTENT", "SUBMIT_ASSIGNMENT", "LOGOUT"]

# Generate base and anomaly activity events
for i in range(1, NUM_EVENTS + 1):
    evt_id = f"EVT-GEN-{i:06d}"
    anomaly_chance = random.random()
    
    # Inject Edge Case 1: Activity from an unenrolled learner
    if anomaly_chance < 0.02:
        lrn = f"LRN-UNENROLLED-{random.randint(999, 9999)}"
        crs = random.choice(courses)["course_id"]
        events.append({
            "event_id": evt_id,
            "enrollment_id": f"ENR-{lrn}-{crs}",
            "event_type": "VIEW_CONTENT",
            "timestamp": "2026-06-01 12:00:00"
        })
        ground_truth.append({
            "target_id": evt_id,
            "anomaly_type": "ACTIVITY_FROM_UNENROLLED_LEARNER",
            "description": "Activity recorded for a user account without a matching valid core enrollment record."
        })
        
    # Inject Edge Case 2: Duplicate events inflating engagement
    elif anomaly_chance < 0.05 and len(enrollments) > 0:
        enr = random.choice(enrollments)["enrollment_id"]
        ts = "2026-07-15 08:30:00"
        # Append main event
        events.append({"event_id": evt_id, "enrollment_id": enr, "event_type": "VIEW_CONTENT", "timestamp": ts})
        # Append immediate duplicate inflation
        dup_id = f"EVT-DUP-{i:06d}"
        events.append({"event_id": dup_id, "enrollment_id": enr, "event_type": "VIEW_CONTENT", "timestamp": ts})
        
        ground_truth.append({
            "target_id": dup_id,
            "anomaly_type": "DUPLICATE_INFLATED_ENGAGEMENT",
            "description": "Identical timestamp and type duplicate event artificially skewing telemetry metrics metrics."
        })
        
    # Normal Baseline Path
    elif len(enrollments) > 0:
        enr = random.choice(enrollments)["enrollment_id"]
        base_date = datetime(2026, 1, 1) + timedelta(days=random.randint(0, 250), hours=random.randint(0, 23))
        events.append({
            "event_id": f"EVT-{enr}-{i:02d}",
            "enrollment_id": enr,
            "event_type": random.choice(event_types),
            "timestamp": base_date.strftime("%Y-%m-%d %H:%M:%S")
        })

# -------------------------------------------------------------
# STEP 6 & 9: OUTCOMES & FILE EXPORT
# -------------------------------------------------------------
os.makedirs("output", exist_ok=True)

def write_csv(filename, data, fields):
    with open(os.path.join("output", filename), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

write_csv("learners.csv", learners, ["learner_id", "name", "email", "cohort"])
write_csv("courses.csv", courses, ["course_id", "title", "category"])
write_csv("content_items.csv", content_items, ["content_id", "course_id", "type"])
write_csv("enrollments.csv", enrollments, ["enrollment_id", "learner_id", "course_id", "enrollment_date"])
write_csv("activity_events.csv", events, ["event_id", "enrollment_id", "event_type", "timestamp"])
write_csv("ground_truth.csv", ground_truth, ["target_id", "anomaly_type", "description"])

print("Success! All deterministic synthetic seed tables exported cleanly to the '/output' directory.")
