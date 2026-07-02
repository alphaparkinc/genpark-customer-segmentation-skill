"""
example_usage.py -- Demonstrates the CustomerSegmentationClient SDK.
"""
from client import CustomerSegmentationClient
import random

def generate_customers(n=200, seed=42):
    random.seed(seed)
    customers = []
    profiles = [
        {"recency_range": (1,20), "freq_range": (10,30), "monetary_range": (500,2000)},
        {"recency_range": (15,45), "freq_range": (4,12), "monetary_range": (150,600)},
        {"recency_range": (60,180), "freq_range": (2,6), "monetary_range": (80,300)},
        {"recency_range": (180,365), "freq_range": (1,3), "monetary_range": (20,100)},
    ]
    for i in range(n):
        p = profiles[i % len(profiles)]
        customers.append({
            "customer_id": f"C{i:04d}",
            "recency_days": random.randint(*p["recency_range"]),
            "frequency": random.randint(*p["freq_range"]),
            "monetary_value": round(random.uniform(*p["monetary_range"]), 2),
        })
    return customers

def main():
    client = CustomerSegmentationClient(seed=42)
    customers = generate_customers(200)

    print("[Customer Segmentation -- RFM K-Means]")
    result = client.segment(customers, n_segments=4)

    print(f"Silhouette Score: {result['silhouette_score']} (higher = better separation)")
    print(f"Features Used: {result['features_used']}")
    print(f"\nSegment Summary:")
    for seg in sorted(result["segments"], key=lambda s: s["avg_monetary"], reverse=True):
        print(f"\n  {seg['label']}")
        print(f"    Customers: {seg['customer_count']}")
        print(f"    Avg Recency: {seg['avg_recency_days']} days | Avg Frequency: {seg['avg_frequency']} orders | Avg Spend: ${seg['avg_monetary']:,.2f}")
        print(f"    Strategy: {seg['strategy']}")

    print(f"\nSample Customer Assignments:")
    for c in result["customers"][:8]:
        print(f"  {c['customer_id']} | R:{c['recency_days']}d F:{c['frequency']} M:${c['monetary_value']:.0f} -> {c['segment']}")

if __name__ == "__main__":
    main()
