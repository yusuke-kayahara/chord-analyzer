import React from 'react';
import { AnalysisResponse, SelectedBorrowedKeys } from '../types/chord';

interface AnalysisResultProps {
  result: AnalysisResponse;
  selectedBorrowedKeys: SelectedBorrowedKeys;
  onBorrowedKeySelect: (chord: string, key: string) => void;
}

const AnalysisResult: React.FC<AnalysisResultProps> = ({ result, selectedBorrowedKeys, onBorrowedKeySelect }) => {
  const formatConfidence = (confidence: number): string => {
    return `${(confidence * 100).toFixed(1)}%`;
  };

  const getConfidenceColor = (confidence: number): string => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getRelationshipBadgeColor = (relationship: string): string => {
    if (relationship.includes('Parallel')) return 'bg-purple-100 text-purple-800';
    if (relationship.includes('Relative')) return 'bg-blue-100 text-blue-800';
    if (relationship.includes('Dominant')) return 'bg-red-100 text-red-800';
    if (relationship.includes('Subdominant')) return 'bg-green-100 text-green-800';
    return 'bg-gray-100 text-gray-800';
  };

  const getAlgorithmName = (algorithm: string): string => {
    switch (algorithm) {
      case 'traditional':
        return '調性感類似度最大化';
      case 'borrowed_chord_minimal':
        return '借用和音数最小化';
      case 'triad_ratio':
        return 'トライアド比率最大化';
      case 'manual':
        return '手動指定';
      case 'hybrid':
        return '複合最適化';
      default:
        return algorithm;
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      {/* メインキー表示 */}
      <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-blue-50 rounded-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">分析結果</h2>
        <div className="flex items-center space-x-4 mb-3">
          <div>
            <span className="text-sm text-gray-600">推定キー:</span>
            <span className="ml-2 text-2xl font-bold text-blue-700">
              {result.main_key}
            </span>
          </div>
          <div>
            <span className="text-sm text-gray-600">信頼度:</span>
            <span className={`ml-2 text-xl font-semibold ${getConfidenceColor(result.confidence)}`}>
              {formatConfidence(result.confidence)}
            </span>
          </div>
        </div>
        <div className="text-xs text-gray-500">
          使用アルゴリズム: {getAlgorithmName(result.algorithm_used)}
        </div>
      </div>

      {/* アルゴリズム比較（複数結果がある場合） */}
      {result.key_candidates && result.key_candidates.length > 1 && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">アルゴリズム比較</h3>
          <div className="grid gap-2">
            {result.key_candidates.map((candidate, index) => (
              <div
                key={index}
                className={`p-3 rounded border ${
                  candidate.key === result.main_key 
                    ? 'bg-blue-100 border-blue-300' 
                    : 'bg-white border-gray-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className={`font-semibold ${
                      candidate.key === result.main_key ? 'text-blue-700' : 'text-gray-700'
                    }`}>
                      {candidate.key}
                    </span>
                    <span className="text-xs text-gray-500">
                      {getAlgorithmName(candidate.algorithm)}
                    </span>
                    {candidate.key === result.main_key && (
                      <span className="text-xs bg-blue-200 text-blue-800 px-2 py-1 rounded">
                        選択
                      </span>
                    )}
                  </div>
                  <div className="flex items-center space-x-3 text-sm">
                    <span className={getConfidenceColor(candidate.confidence)}>
                      {formatConfidence(candidate.confidence)}
                    </span>
                    <span className="text-gray-600">
                      借用: {candidate.borrowed_chord_count}個
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ピッチクラスベクトル表示 */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">構成音分布</h3>
        <div className="grid grid-cols-12 gap-1">
          {['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'].map((note, index) => {
            const value = result.pitch_class_vector[index];
            const height = Math.max(value * 100, 2); // 最小2%の高さ
            return (
              <div key={note} className="text-center">
                <div 
                  className="bg-blue-500 mb-1 rounded-t"
                  style={{ height: `${height}px` }}
                ></div>
                <div className="text-xs font-medium text-gray-600">{note}</div>
                <div className="text-xs text-gray-400">
                  {(value * 100).toFixed(0)}%
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 借用和音表示 */}
      {result.borrowed_chords.length > 0 ? (
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            借用和音 ({result.borrowed_chords.length}個検出)
          </h3>
          <div className="space-y-4">
            {result.borrowed_chords.map((borrowed, index) => (
              <div key={index} className="border border-amber-200 rounded-lg p-4 bg-amber-50">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-xl font-bold text-amber-700">
                    {borrowed.chord}
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {borrowed.non_diatonic_notes.map((note, noteIndex) => (
                      <span
                        key={noteIndex}
                        className="px-2 py-1 bg-red-100 text-red-800 text-xs font-medium rounded"
                      >
                        {note}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h5 className="text-sm font-medium text-gray-700">借用元候補:</h5>
                    {selectedBorrowedKeys[borrowed.chord] && (
                      <button
                        onClick={() => onBorrowedKeySelect(borrowed.chord, '')}
                        className="text-xs text-gray-500 hover:text-blue-600 underline"
                      >
                        自動選択に戻す
                      </button>
                    )}
                  </div>
                  <div className="space-y-2">
                    {borrowed.source_candidates.map((candidate, candIndex) => {
                      const isSelected = selectedBorrowedKeys[borrowed.chord] === candidate.key;
                      const isAutoSelected = !selectedBorrowedKeys[borrowed.chord] && candIndex === 0;
                      return (
                        <div
                          key={candIndex}
                          onClick={() => onBorrowedKeySelect(borrowed.chord, candidate.key)}
                          className={`flex items-center justify-between p-3 rounded border transition-colors cursor-pointer hover:shadow-md ${
                            isSelected ? 'bg-blue-100 border-blue-300 ring-2 ring-blue-200' : 
                            isAutoSelected ? 'bg-green-50 border-green-200 hover:bg-green-100' : 
                            'bg-white border-gray-200 hover:bg-gray-50'
                          }`}
                        >
                          <div className="flex items-center space-x-3">
                            <span className={`font-semibold ${
                              isSelected ? 'text-blue-800' : 
                              isAutoSelected ? 'text-green-800' : 
                              'text-gray-800'
                            }`}>
                              {candidate.key}
                            </span>
                            <span
                              className={`px-2 py-1 rounded-full text-xs font-medium ${getRelationshipBadgeColor(candidate.relationship)}`}
                            >
                              {candidate.relationship}
                            </span>
                            {isSelected && (
                              <span className="text-xs bg-blue-200 text-blue-800 px-2 py-1 rounded">
                                選択中
                              </span>
                            )}
                            {isAutoSelected && (
                              <span className="text-xs bg-green-200 text-green-800 px-2 py-1 rounded">
                                自動選択
                              </span>
                            )}
                          </div>
                          <div className={`font-semibold ${getConfidenceColor(candidate.confidence)}`}>
                            {formatConfidence(candidate.confidence)}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="p-4 bg-green-50 rounded-lg">
          <h3 className="text-lg font-semibold text-green-800 mb-2">
            借用和音は検出されませんでした
          </h3>
          <p className="text-green-700">
            すべてのコードが{result.main_key}のダイアトニック和音です。
          </p>
        </div>
      )}

      {/* 音楽理論解説 */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-sm font-medium text-gray-800 mb-2">音楽理論解説</h3>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• <strong>借用和音</strong>: メインキーの外から「借りてきた」和音</li>
          <li>• <strong>Parallel Minor/Major</strong>: 同じルートの短調/長調から借用</li>
          <li>• <strong>Secondary Dominant</strong>: 他のキーのドミナント機能を借用</li>
          <li>• <strong>信頼度</strong>: 借用元キーでの構成音の適合度</li>
        </ul>
      </div>
    </div>
  );
};

export default AnalysisResult;