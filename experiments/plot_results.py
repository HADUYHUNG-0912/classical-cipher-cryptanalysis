import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"

def plot_caesar():
    csv_file = RESULTS_DIR / "caesar_results.csv"
    if not csv_file.exists():
        print("Không tìm thấy kết quả Caesar.")
        return

    df = pd.read_csv(csv_file)
    L = df["Do dai L"]
    time_ms = df["TB thoi gian (ms)"]
    acc = df["Ti le pha dung (%)"]

    fig, ax1 = plt.subplots(figsize=(8, 5))

    color = 'tab:red'
    ax1.set_xlabel('Độ dài văn bản L (ký tự)')
    ax1.set_ylabel('Thời gian chạy (ms)', color=color)
    ax1.plot(L, time_ms, marker='o', color=color, linewidth=2, label='Thời gian (ms)')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Tỉ lệ phá mã thành công (%)', color=color)
    ax2.plot(L, acc, marker='s', color=color, linewidth=2, linestyle='--', label='Tỉ lệ đúng (%)')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([0, 110])

    plt.title('Hiệu suất phá mã CAESAR CIPHER')
    fig.tight_layout()

    out_file = RESULTS_DIR / "caesar_chart.png"
    plt.savefig(out_file, dpi=300)
    print(f"Saved chart to: {out_file}")

if __name__ == "__main__":
    plot_caesar()
