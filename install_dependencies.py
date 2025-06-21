#!/usr/bin/env python3
"""
依存関係のない簡易版コード進行分析API
pychordやnumpyの代わりに基本的な実装を使用
"""
import json
import re
from typing import List, Dict, Tuple
import math

# 音名とピッチクラスの対応
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# 基本的なコード構成音の定義
CHORD_TEMPLATES = {
    'M': [0, 4, 7],       # メジャートライアド
    'm': [0, 3, 7],       # マイナートライアド  
    '7': [0, 4, 7, 10],   # ドミナント7th
    'M7': [0, 4, 7, 11],  # メジャー7th
    'm7': [0, 3, 7, 10],  # マイナー7th
    'mM7': [0, 3, 7, 11], # マイナーメジャー7th
    'dim': [0, 3, 6],     # ディミニッシュ
    'aug': [0, 4, 8],     # オーギュメント
    'sus4': [0, 5, 7],    # サス4
    'sus2': [0, 2, 7],    # サス2
}

# Krumhanslの調性感プロファイル
KRUMHANSL_MAJOR = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KRUMHANSL_MINOR = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

def extract_chords(chord_input: str) -> List[str]:
    """[]で囲まれたコードを抽出"""
    pattern = r'\[([^\]]+)\]'
    return re.findall(pattern, chord_input)

def parse_chord(chord_symbol: str) -> Tuple[str, str]:
    """コードシンボルをルートとタイプに分解"""
    # 基本的なパターンマッチング
    if 'mM7' in chord_symbol:
        root = chord_symbol.replace('mM7', '')
        return root, 'mM7'
    elif 'M7' in chord_symbol:
        root = chord_symbol.replace('M7', '')
        return root, 'M7'
    elif 'm7' in chord_symbol:
        root = chord_symbol.replace('m7', '')
        return root, 'm7'
    elif chord_symbol.endswith('7'):
        root = chord_symbol[:-1]
        return root, '7'
    elif chord_symbol.endswith('m'):
        root = chord_symbol[:-1]
        return root, 'm'
    else:
        # メジャートライアドまたは不明
        return chord_symbol, 'M'

def note_to_pitch_class(note: str) -> int:
    """音名をピッチクラス番号に変換"""
    # フラットをシャープに変換
    replacements = {
        'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 
        'Ab': 'G#', 'Bb': 'A#'
    }
    note = replacements.get(note, note)
    
    return NOTES.index(note) if note in NOTES else 0

def get_chord_components(chord_symbol: str) -> List[str]:
    """コードの構成音を取得（簡易版）"""
    root, chord_type = parse_chord(chord_symbol)
    
    if chord_type not in CHORD_TEMPLATES:
        chord_type = 'M'  # デフォルトはメジャー
    
    root_pc = note_to_pitch_class(root)
    intervals = CHORD_TEMPLATES[chord_type]
    
    notes = []
    for interval in intervals:
        pc = (root_pc + interval) % 12
        notes.append(NOTES[pc])
    
    return notes

def create_pitch_class_vector(chords: List[str]) -> List[float]:
    """12次元ピッチクラスベクトルを作成"""
    vector = [0.0] * 12
    
    for chord_symbol in chords:
        notes = get_chord_components(chord_symbol)
        for note in notes:
            pitch_class = note_to_pitch_class(note)
            vector[pitch_class] += 1
    
    # 正規化
    total = sum(vector)
    if total > 0:
        vector = [v / total for v in vector]
    
    return vector

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """コサイン類似度を計算"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(a * a for a in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    return dot_product / (magnitude1 * magnitude2)

def rotate_profile(profile: List[float], root: int) -> List[float]:
    """キープロファイルを回転"""
    return profile[root:] + profile[:root]

def find_best_key(pitch_vector: List[float]) -> Tuple[str, float]:
    """最適なキーを見つける"""
    best_similarity = -1
    best_key = "C Major"
    
    for root in range(12):
        # メジャーキーとの比較
        major_profile = rotate_profile(KRUMHANSL_MAJOR, root)
        similarity = cosine_similarity(pitch_vector, major_profile)
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_key = f"{NOTES[root]} Major"
        
        # マイナーキーとの比較
        minor_profile = rotate_profile(KRUMHANSL_MINOR, root)
        similarity = cosine_similarity(pitch_vector, minor_profile)
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_key = f"{NOTES[root]} Minor"
    
    return best_key, best_similarity

def analyze_chord_progression(chord_input: str) -> Dict:
    """コード進行を分析"""
    chords = extract_chords(chord_input)
    
    if not chords:
        return {
            "main_key": "Unknown",
            "confidence": 0.0,
            "borrowed_chords": [],
            "pitch_class_vector": [0.0] * 12
        }
    
    pitch_vector = create_pitch_class_vector(chords)
    main_key, confidence = find_best_key(pitch_vector)
    
    return {
        "main_key": main_key,
        "confidence": confidence,
        "borrowed_chords": [],  # Phase 2で実装
        "pitch_class_vector": pitch_vector
    }

# テスト実行
if __name__ == "__main__":
    print("=== 簡易版コード進行分析 ===")
    
    test_cases = [
        "[CM7][Am7][FM7][G7]",
        "[FM7][FmM7][Em7][A7]",
        "[C][F][G][C]",
        "[Am][F][C][G]",
    ]
    
    for test_input in test_cases:
        print(f"\n入力: {test_input}")
        result = analyze_chord_progression(test_input)
        print(f"推定キー: {result['main_key']}")
        print(f"信頼度: {result['confidence']:.3f}")
        print(f"ピッチクラスベクトル: {[round(v, 3) for v in result['pitch_class_vector']]}")
    
    print("\n✓ 基本的な分析機能が動作しています")
    print("✓ 次はFastAPIサーバーでの実装に進めます")