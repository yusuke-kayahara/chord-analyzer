import React from 'react';
import { BorrowedChord } from '../types/chord';

interface ChordVisualizationProps {
  chordInput: string;
  mainKey: string;
  borrowedChords: BorrowedChord[];
}

const ChordVisualization: React.FC<ChordVisualizationProps> = ({
  chordInput,
  mainKey,
  borrowedChords
}) => {
  // コード進行を抽出
  const extractChords = (input: string): string[] => {
    const pattern = /\[([^\]]+)\]/g;
    const matches = [];
    let match;
    while ((match = pattern.exec(input)) !== null) {
      matches.push(match[1]);
    }
    return matches;
  };

  const chords = extractChords(chordInput);
  const borrowedChordNames = borrowedChords.map(bc => bc.chord);

  // コードが借用和音かどうかを判定
  const isBorrowedChord = (chord: string): boolean => {
    return borrowedChordNames.includes(chord);
  };

  // 借用和音の詳細情報を取得
  const getBorrowedInfo = (chord: string): BorrowedChord | undefined => {
    return borrowedChords.find(bc => bc.chord === chord);
  };

  // コード進行の度数分析（簡易版）
  const analyzeChordFunction = (chord: string): string => {
    // 簡易的な度数分析（実際にはより複雑な処理が必要）
    const keyRoot = mainKey.split(' ')[0];
    const keyType = mainKey.split(' ')[1];
    
    // C Majorキーでの度数マッピング（簡易版）
    const majorDegrees: { [key: string]: string } = {
      'C': 'I', 'Dm': 'ii', 'Em': 'iii', 'F': 'IV', 'G': 'V', 'Am': 'vi', 'Bdim': 'vii°'
    };
    
    // より完全な実装が必要だが、ここでは基本的なマッピング
    if (keyRoot === 'C' && keyType === 'Major') {
      const found = Object.entries(majorDegrees).find(([chordName]) => 
        chord.startsWith(chordName)
      );
      if (found) return found[1];
    }
    
    return '?';
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">
        コード進行視覚化
      </h3>
      
      {/* キー情報 */}
      <div className="mb-4 p-3 bg-blue-50 rounded-lg">
        <span className="text-sm text-blue-600 font-medium">Key: </span>
        <span className="text-lg font-bold text-blue-700">{mainKey}</span>
      </div>

      {/* コード進行表示 */}
      <div className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-2">
          {chords.map((chord, index) => {
            const isBorrowed = isBorrowedChord(chord);
            const borrowedInfo = getBorrowedInfo(chord);
            const degree = analyzeChordFunction(chord);
            
            return (
              <div
                key={index}
                className={`
                  relative p-3 rounded-lg border-2 transition-all duration-200 hover:scale-105
                  ${isBorrowed 
                    ? 'bg-amber-50 border-amber-300 shadow-md' 
                    : 'bg-blue-50 border-blue-200 hover:bg-blue-100'
                  }
                `}
              >
                {/* コード名 */}
                <div className={`text-center font-bold text-lg ${
                  isBorrowed ? 'text-amber-700' : 'text-blue-700'
                }`}>
                  {chord}
                </div>
                
                {/* 度数表示 */}
                <div className="text-center text-xs text-gray-600 mt-1">
                  {degree}
                </div>
                
                {/* 借用和音インジケーター */}
                {isBorrowed && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-amber-500 rounded-full"></div>
                )}
                
                {/* 非ダイアトニック音表示 */}
                {borrowedInfo && (
                  <div className="mt-2 flex flex-wrap gap-1 justify-center">
                    {borrowedInfo.non_diatonic_notes.map((note, noteIndex) => (
                      <span
                        key={noteIndex}
                        className="px-1 py-0.5 bg-red-100 text-red-700 text-xs rounded"
                      >
                        {note}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* 進行矢印 */}
        <div className="flex justify-center items-center space-x-4 mt-4">
          {chords.slice(0, -1).map((_, index) => (
            <div key={index} className="flex items-center">
              <div className="w-8 h-0.5 bg-gray-300"></div>
              <svg 
                className="w-4 h-4 text-gray-400 ml-1" 
                fill="currentColor" 
                viewBox="0 0 20 20"
              >
                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
            </div>
          ))}
        </div>
      </div>

      {/* 凡例 */}
      <div className="mt-6 flex flex-wrap gap-4 text-sm">
        <div className="flex items-center">
          <div className="w-4 h-4 bg-blue-100 border border-blue-200 rounded mr-2"></div>
          <span className="text-gray-600">ダイアトニック和音</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-amber-100 border border-amber-300 rounded mr-2 relative">
            <div className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-amber-500 rounded-full"></div>
          </div>
          <span className="text-gray-600">借用和音</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-2 bg-red-100 rounded mr-2"></div>
          <span className="text-gray-600">非ダイアトニック音</span>
        </div>
      </div>
    </div>
  );
};

export default ChordVisualization;