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

def plot_vigenere():
    csv_file = RESULTS_DIR / "vigenere_ic_detailed_results.csv"
    if not csv_file.exists():
        print("Không tìm thấy kết quả Vigenere.")
        return

    df = pd.read_csv(csv_file)
    
    # Chart 1: IC Accuracy vs Key Length for different L
    plt.figure(figsize=(10, 6))
    for L in sorted(df['Text_Length'].unique()):
        sub_df = df[df['Text_Length'] == L]
        plt.plot(sub_df['Key_Length'], sub_df['IC_Accuracy_Pct'], marker='o', label=f'L = {L}')
    
    plt.title('Độ chính xác của hàm ước lượng IC theo Độ dài khóa (Key Length)')
    plt.xlabel('Độ dài khóa (Key Length)')
    plt.ylabel('Độ chính xác IC (%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.ylim([-5, 105])
    plt.tight_layout()
    
    out_file1 = RESULTS_DIR / "vigenere_ic_chart.png"
    plt.savefig(out_file1, dpi=300)
    plt.close()
    print(f"Saved chart to: {out_file1}")

    # Chart 2: Key Recovery Rate vs Key Length for different L
    plt.figure(figsize=(10, 6))
    for L in sorted(df['Text_Length'].unique()):
        sub_df = df[df['Text_Length'] == L]
        plt.plot(sub_df['Key_Length'], sub_df['Key_Recovery_Pct'], marker='s', linestyle='--', label=f'L = {L}')
    
    plt.title('Tỉ lệ khôi phục chính xác 100% Khóa (Key Recovery Rate) theo Key Length')
    plt.xlabel('Độ dài khóa (Key Length)')
    plt.ylabel('Tỉ lệ phá khóa thành công (%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.ylim([-5, 105])
    plt.tight_layout()

    out_file2 = RESULTS_DIR / "vigenere_key_recovery_chart.png"
    plt.savefig(out_file2, dpi=300)
    plt.close()
    print(f"Saved chart to: {out_file2}")


if __name__ == "__main__":
    plot_caesar()
    plot_vigenere()
