import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def perform_eda():
    try:
        df = pd.read_csv("crop_results.csv")
    except FileNotFoundError:
        print("⚠️  No data yet! Run detector.py first.")
        return

    print("\n📊 EDA REPORT")
    print("=" * 40)
    print(f"Total crops analyzed  : {len(df)}")
    print(f"Unique plants found   : {df['plant_name'].nunique()}")
    print(f"Average confidence    : {df['confidence'].mean():.2f}%")
    print(f"\nStatus breakdown:")
    print(df['status'].value_counts())
    print(f"\nTop 5 detected plants:")
    print(df['plant_name'].value_counts().head())

    # ── Chart 1: Status Pie Chart ─────────────────
    plt.figure(figsize=(5, 5))
    df['status'].value_counts().plot.pie(
        autopct='%1.1f%%',
        colors=['#2ecc71', '#f39c12'],
        startangle=90
    )
    plt.title("Crop Health Status")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("chart_status.png")
    plt.show()

    # ── Chart 2: Top Plants Bar Chart ────────────
    plt.figure(figsize=(8, 4))
    df['plant_name'].value_counts().head(10).plot(
        kind='bar', color='#3498db'
    )
    plt.title("Top 10 Detected Plants")
    plt.xlabel("Plant Name")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("chart_plants.png")
    plt.show()

    # ── Chart 3: Confidence Distribution ─────────
    plt.figure(figsize=(7, 4))
    sns.histplot(df['confidence'], bins=10,
                 color='#9b59b6', kde=True)
    plt.title("Confidence Score Distribution")
    plt.xlabel("Confidence %")
    plt.tight_layout()
    plt.savefig("chart_confidence.png")
    plt.show()

    print("\n✅ Charts saved!")

if __name__ == "__main__":
    perform_eda()