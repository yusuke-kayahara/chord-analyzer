#!/usr/bin/env python3
"""
キー関係性ボーナスシステムの設計
"""

def design_key_relationship_bonus():
    print("=== キー関係性ボーナスシステムの設計 ===\n")
    
    print("1. 音楽理論的なキー関係性の分類:")
    print()
    
    # キー関係性の分類と重要度
    key_relationships = {
        "最重要関係": {
            "Parallel Minor/Major": 0.15,          # 同主調（CメジャーとCマイナー）
            "Parallel Harmonic Minor": 0.12,      # パラレルハーモニックマイナー
            "Relative Minor": 0.10,               # 関係調（CメジャーとAマイナー）
            "Relative Major": 0.10,               # 関係調（AマイナーとCメジャー）
        },
        "重要関係": {
            "Dominant Relationship": 0.08,         # 属調（Cメジャーとgメジャー）
            "Subdominant Relationship": 0.08,     # 下属調（CメジャーとFメジャー）
        },
        "中程度関係": {
            "Major 2nd": 0.05,                    # 全音上（Cメジャーとdメジャー）
            "Minor 2nd": 0.03,                    # 半音上
            "Minor 3rd": 0.04,                    # 短3度上
            "Major 3rd": 0.04,                    # 長3度上
        },
        "その他": {
            "default": 0.00                       # その他の関係
        }
    }
    
    for category, relationships in key_relationships.items():
        print(f"{category}:")
        for relationship, bonus in relationships.items():
            print(f"  {relationship:>25} → +{bonus:.2f} ボーナス")
        print()
    
    print("2. 実装方針:")
    print("   - analyze_relationship()で関係性を判定")
    print("   - get_key_relationship_bonus()で関係性ボーナスを計算")
    print("   - calculate_key_confidence()でボーナスを適用")
    print("   - 最大ボーナスは0.15（15%）に制限")
    
    print()
    print("3. 適用例（Cメジャーキーからの借用）:")
    examples = [
        ("Fm", "C Minor", "Parallel Minor/Major", "+0.15"),
        ("Fm", "C Harmonic Minor", "Parallel Harmonic Minor", "+0.12"),
        ("Fm", "Ab Major", "Relative Major", "+0.10"),
        ("F#dim", "A Minor", "Relative Minor", "+0.10"),
        ("Bb", "F Major", "Subdominant Relationship", "+0.08"),
        ("F#m", "D Major", "Major 2nd", "+0.05"),
        ("Fm", "Eb Major", "Minor 3rd", "+0.04"),
    ]
    
    for chord, source_key, relationship, bonus in examples:
        print(f"   {chord:>6} from {source_key:>15} ({relationship:>25}) → {bonus}")
    
    print()
    print("4. 実装上の注意点:")
    print("   - ボーナスは信頼度の最終計算で適用")
    print("   - 1.0を超えないよう上限制御")
    print("   - 既存のコンテキストボーナスと併用")
    print("   - 関係性の判定は既存のanalyze_relationship()を活用")

def test_key_relationship_examples():
    print("\n=== キー関係性の具体例テスト ===\n")
    
    test_cases = [
        # Cメジャーキーからの借用例
        ("C Major", "C Minor", "Parallel Minor/Major"),
        ("C Major", "C Harmonic Minor", "Parallel Harmonic Minor"),
        ("C Major", "A Minor", "Relative Minor"),
        ("C Major", "G Major", "Dominant Relationship"),
        ("C Major", "F Major", "Subdominant Relationship"),
        ("C Major", "D Major", "Major 2nd"),
        ("C Major", "Eb Major", "Minor 3rd"),
        
        # Aマイナーキーからの借用例
        ("A Minor", "A Major", "Parallel Minor/Major"),
        ("A Minor", "A Harmonic Minor", "同一キー"),
        ("A Minor", "C Major", "Relative Major"),
        ("A Minor", "E Minor", "Dominant Relationship"),
        ("A Minor", "D Minor", "Subdominant Relationship"),
    ]
    
    def get_expected_bonus(relationship):
        bonus_map = {
            "Parallel Minor/Major": 0.15,
            "Parallel Harmonic Minor": 0.12,
            "Relative Minor": 0.10,
            "Relative Major": 0.10,
            "Dominant Relationship": 0.08,
            "Subdominant Relationship": 0.08,
            "Major 2nd": 0.05,
            "Minor 3rd": 0.04,
            "同一キー": 0.00
        }
        return bonus_map.get(relationship, 0.00)
    
    print("メインキー → 借用元キー (関係性) → 期待ボーナス")
    for main_key, source_key, expected_relationship in test_cases:
        expected_bonus = get_expected_bonus(expected_relationship)
        print(f"{main_key:>8} → {source_key:>15} ({expected_relationship:>25}) → +{expected_bonus:.2f}")

if __name__ == "__main__":
    design_key_relationship_bonus()
    test_key_relationship_examples()