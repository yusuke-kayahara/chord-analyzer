// コード進行分析のTypeScript型定義
export interface ChordAnalysisRequest {
  chord_input: string;
}

export interface KeyCandidate {
  key: string;
  relationship: string;
  confidence: number;
}

export interface BorrowedChord {
  chord: string;
  non_diatonic_notes: string[];
  source_candidates: KeyCandidate[];
}

export interface ChordAnalysisResponse {
  main_key: string;
  confidence: number;
  borrowed_chords: BorrowedChord[];
  pitch_class_vector: number[];
}

export interface UIState {
  isAnalyzing: boolean;
  error: string | null;
  result: ChordAnalysisResponse | null;
}