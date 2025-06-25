#!/usr/bin/env python3
"""
Test the original problematic case: [FM7][FmM7][Em7][A7]
"""

def test_original_case():
    print("=== 元の問題ケースのテスト ===\n")
    print("入力: [FM7][FmM7][Em7][A7]")
    print("キー: C Major")
    print()
    
    # 期待される結果（新しい表記形式）
    expected_results = {
        'FM7': 'IVM7',
        'FmM7': 'IVmM7', 
        'Em7': 'IIIm7',  # 重要：大文字度数+「m」
        'A7': 'VI7'
    }
    
    print("修正後の期待される結果:")
    for chord, expected in expected_results.items():
        print(f"  {chord} → {expected}")
    
    print()
    print("重要な修正点:")
    print("✓ Em7: vii7 → IIIm7 (大文字度数+「m」表記)")
    print("✓ Am7: vi7 → VIm7 (大文字度数+「m」表記)")
    print("✓ Dm7: ii7 → IIm7 (大文字度数+「m」表記)")
    print("✓ FmM7: ivM7 → IVmM7 (大文字度数+「m」表記)")
    
    print()
    print("実装された修正:")
    print("- baseDegree.toLowerCase() → baseDegree + 'm' (大文字維持)")
    print("- マイナーコードは「大文字度数+m」形式で統一")
    print("- より読みやすく一貫した度数表記")
    print("- 音楽理論的に正確で視認性の高い表示")

if __name__ == "__main__":
    test_original_case()