import React, { useState, useEffect } from 'react';
import { AnalysisHistory as AnalysisHistoryType, AdvancedSettings } from '../types/chord';
import { HistoryStorage } from '../utils/historyStorage';

interface AnalysisHistoryProps {
  onReplayAnalysis: (chordInput: string, settings: AdvancedSettings) => void;
}

const AnalysisHistory: React.FC<AnalysisHistoryProps> = ({ onReplayAnalysis }) => {
  const [history, setHistory] = useState<AnalysisHistoryType[]>([]);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = () => {
    const historyData = HistoryStorage.getHistory();
    setHistory(historyData);
  };

  const handleReplay = (item: AnalysisHistoryType) => {
    const settings: AdvancedSettings = {
      algorithm: item.settings.algorithm,
      traditional_weight: item.settings.traditional_weight,
      borrowed_chord_weight: item.settings.borrowed_chord_weight,
      triad_ratio_weight: item.settings.triad_ratio_weight,
      manual_key: item.settings.manual_key,
      showAdvanced: false
    };
    
    onReplayAnalysis(item.chord_input, settings);
  };

  const handleRemoveItem = (id: string, event: React.MouseEvent) => {
    event.stopPropagation(); // クリックイベントの伝播を停止
    HistoryStorage.removeItem(id);
    loadHistory();
  };

  const handleClearHistory = () => {
    if (window.confirm('分析履歴をすべて削除しますか？')) {
      HistoryStorage.clearHistory();
      loadHistory();
    }
  };

  const formatTimestamp = (timestamp: number): string => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - timestamp;
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffMinutes < 1) return 'たった今';
    if (diffMinutes < 60) return `${diffMinutes}分前`;
    if (diffHours < 24) return `${diffHours}時間前`;
    if (diffDays < 7) return `${diffDays}日前`;
    
    return date.toLocaleDateString('ja-JP', { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getAlgorithmName = (algorithm: string): string => {
    switch (algorithm) {
      case 'traditional': return 'Krumhansl';
      case 'borrowed_chord_minimal': return '借用最小';
      case 'triad_ratio': return 'トライアド';
      case 'manual': return '手動指定';
      case 'hybrid': return 'ハイブリッド';
      default: return algorithm;
    }
  };

  if (history.length === 0) {
    return null; // 履歴がない場合は表示しない
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center space-x-2 text-gray-700 hover:text-gray-900"
        >
          <svg 
            className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
          <h3 className="text-lg font-semibold">分析履歴 ({history.length}件)</h3>
        </button>
        
        {history.length > 0 && (
          <button
            onClick={handleClearHistory}
            className="text-xs text-gray-500 hover:text-red-600 transition-colors"
          >
            履歴をクリア
          </button>
        )}
      </div>

      {isExpanded && (
        <div className="space-y-2">
          {history.map((item) => (
            <div
              key={item.id}
              onClick={() => handleReplay(item)}
              className="p-3 border border-gray-200 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors group"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <span className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">
                      {item.chord_input}
                    </span>
                    <span className="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded">
                      {getAlgorithmName(item.settings.algorithm)}
                    </span>
                    {item.settings.manual_key && (
                      <span className="text-xs text-purple-600 bg-purple-100 px-2 py-1 rounded">
                        {item.settings.manual_key}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center space-x-4 mt-2 text-xs text-gray-600">
                    <span>推定: {item.result.main_key}</span>
                    <span>借用: {item.result.borrowed_chords.length}個</span>
                    <span>{formatTimestamp(item.timestamp)}</span>
                  </div>
                </div>
                
                <button
                  onClick={(e) => handleRemoveItem(item.id, e)}
                  className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-600 transition-all"
                  title="削除"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
          
          <div className="pt-2 text-xs text-gray-500 text-center">
            クリックで再分析 • 最大{history.length}/10件まで保存
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisHistory;