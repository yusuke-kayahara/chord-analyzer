# コード進行分析WEBアプリ - 借用和音検出システム

## プロジェクト概要
コード進行を入力し、メインキーを推定して借用和音（非ダイアトニックコード）の由来キーを特定するWEBアプリケーションを作成します。

## 核心機能

### メインキー推定
- 12次元ピッチクラスベクトル化による構成音集計
- Krumhanslの調性感プロファイルとのコサイン類似度計算
- 最も類似度が高いキーをメインキーとして出力

### 借用和音検出
- メインキーから外れた非ダイアトニック音の特定
- 借用元キーの候補提示（一致度計算による）
- 部分転調の可能性を示唆

## 処理フロー

### ① フロントエンド入力
```
入力例: [FM7(13)][FmM7][Em7][A7]
形式: []で囲まれたコードネームのみを抽出・分析
```

### ② 構成音抽出（pychord使用）
```python
from pychord import Chord

# 例: FM7(13) → [F, A, C, E, D]
chord = Chord("FM7(13)")
notes = [note.name for note in chord.components()]
```

### ③ ピッチクラスベクトル化
```python
# 12次元ベクトル（C, C#, D, D#, E, F, F#, G, G#, A, A#, B）
def create_pitch_class_vector(all_notes):
    vector = [0] * 12
    for note in all_notes:
        pitch_class = note_to_pitch_class(note)
        vector[pitch_class] += 1
    return normalize(vector)
```

### ④ 調性感プロファイルとの照合
```python
# Krumhanslのメジャーキープロファイル
KRUMHANSL_MAJOR = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KRUMHANSL_MINOR = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

def find_best_key(pitch_vector):
    best_similarity = -1
    best_key = None
    
    for root in range(12):  # 12キー分
        # メジャーキーとの類似度
        major_profile = rotate_profile(KRUMHANSL_MAJOR, root)
        similarity = cosine_similarity(pitch_vector, major_profile)
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_key = f"{NOTES[root]} Major"
            
        # マイナーキーとの類似度
        minor_profile = rotate_profile(KRUMHANSL_MINOR, root)
        similarity = cosine_similarity(pitch_vector, minor_profile)
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_key = f"{NOTES[root]} Minor"
    
    return best_key, best_similarity
```

### ⑤ 非ダイアトニック音の検出
```python
def detect_non_diatonic_notes(chords, main_key):
    diatonic_notes = get_diatonic_notes(main_key)
    non_diatonic_chords = []
    
    for chord_symbol in chords:
        chord = Chord(chord_symbol)
        chord_notes = [note.name for note in chord.components()]
        
        non_diatonic_notes = [note for note in chord_notes 
                             if note not in diatonic_notes]
        
        if non_diatonic_notes:
            non_diatonic_chords.append({
                'chord': chord_symbol,
                'non_diatonic_notes': non_diatonic_notes
            })
    
    return non_diatonic_chords
```

### ⑥ 借用元キー推定
```python
def find_borrowed_sources(non_diatonic_chords, main_key):
    borrowing_candidates = []
    
    for chord_info in non_diatonic_chords:
        chord_notes = Chord(chord_info['chord']).components()
        chord_vector = create_pitch_class_vector(chord_notes)
        
        # 全24キー（メジャー・マイナー）との照合
        for key in ALL_KEYS:
            if key == main_key:
                continue
                
            key_notes = get_diatonic_notes(key)
            if all(note in key_notes for note in chord_notes):
                borrowing_candidates.append({
                    'chord': chord_info['chord'],
                    'source_key': key,
                    'relationship': analyze_relationship(main_key, key)
                })
    
    return borrowing_candidates
```

## 技術スタック

| 層 | 技術 | 役割 |
|---|---|---|
| **フロントエンド** | React + TypeScript + Tailwind CSS | UI/UX、コード入力インターフェース |
| **バックエンド** | Python + FastAPI | 音楽理論計算、pychord活用 |
| **音楽理論処理** | pychord + NumPy + scikit-learn | コード解析、ベクトル計算 |
| **ホスティング** | Vercel (Frontend) + Render/Railway (API) | デプロイメント |

## データ構造

### フロントエンド（TypeScript）
```typescript
interface ChordProgression {
  rawInput: string;           // "[FM7(13)][FmM7][Em7][A7]"
  chords: string[];          // ["FM7(13)", "FmM7", "Em7", "A7"]
  mainKey: string;           // "C Major"
  confidence: number;        // 0.85
  borrowedChords: BorrowedChord[];
}

interface BorrowedChord {
  chord: string;             // "FmM7"
  nonDiatonicNotes: string[]; // ["Ab"]
  sourceCandidates: KeyCandidate[];
}

interface KeyCandidate {
  key: string;               // "F Minor"
  relationship: string;      // "Parallel Minor of IV"
  confidence: number;        // 0.92
}
```

### バックエンド（Python）
```python
from pydantic import BaseModel
from typing import List

class ChordAnalysisRequest(BaseModel):
    chord_input: str

class KeyCandidate(BaseModel):
    key: str
    relationship: str
    confidence: float

class BorrowedChord(BaseModel):
    chord: str
    non_diatonic_notes: List[str]
    source_candidates: List[KeyCandidate]

class AnalysisResponse(BaseModel):
    main_key: str
    confidence: float
    borrowed_chords: List[BorrowedChord]
    pitch_class_vector: List[float]
```

## API設計

### エンドポイント
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_chord_progression(request: ChordAnalysisRequest):
    # ① コード抽出
    chords = extract_chords(request.chord_input)
    
    # ② 構成音抽出・ベクトル化
    pitch_vector = create_pitch_class_vector(chords)
    
    # ③ メインキー推定
    main_key, confidence = find_best_key(pitch_vector)
    
    # ④ 借用和音検出
    borrowed_chords = analyze_borrowed_chords(chords, main_key)
    
    return AnalysisResponse(
        main_key=main_key,
        confidence=confidence,
        borrowed_chords=borrowed_chords,
        pitch_class_vector=pitch_vector.tolist()
    )
```

## 実装手順

### Phase 1: バックエンド基盤
1. FastAPI プロジェクトセットアップ
2. pychord による基本的なコード解析
3. Krumhansl プロファイル実装
4. メインキー推定機能

### Phase 2: 借用和音検出
1. 非ダイアトニック音検出
2. 借用元キー候補算出
3. 音楽理論的関係性分析
4. API エンドポイント完成

### Phase 3: フロントエンド
1. React プロジェクトセットアップ
2. コード入力インターフェース
3. 分析結果表示コンポーネント
4. 視覚化（キー関係図、コード進行表示）

### Phase 4: 統合・デプロイ
1. CORS 設定・API 統合
2. エラーハンドリング
3. デプロイメント（Vercel + Render）
4. テスト・最適化

## 使用例

### 入力
```
[CM7][Am7][FM7][FmM7][Em7][A7][Dm7][G7]
```

### 出力
```json
{
  "main_key": "C Major",
  "confidence": 0.89,
  "borrowed_chords": [
    {
      "chord": "FmM7",
      "non_diatonic_notes": ["Ab"],
      "source_candidates": [
        {
          "key": "C Minor",
          "relationship": "Parallel Minor (iv chord)",
          "confidence": 0.95
        },
        {
          "key": "Ab Major", 
          "relationship": "bVI Key (vi chord)",
          "confidence": 0.78
        }
      ]
    },
    {
      "chord": "A7",
      "non_diatonic_notes": ["C#"],
      "source_candidates": [
        {
          "key": "D Minor",
          "relationship": "Secondary Dominant (V/ii)",
          "confidence": 0.92
        }
      ]
    }
  ]
}
```

## 拡張可能性
- モード分析（ドリアン、リディアンなど）
- ジャズ理論対応（テンションコード、代理コード）
- 確率的転調検出
- リアルタイム分析
- MIDI 入出力対応

このシステムにより、作曲家や音楽理論学習者が複雑なコード進行の構造を直感的に理解できるようになります。