import React from 'react';

interface PianoKeyboardProps {
  activeNotes: string[]; // 例: ["C4", "E4", "G4", "B4"]
  startOctave?: number;
  endOctave?: number;
  className?: string;
}

const PianoKeyboard: React.FC<PianoKeyboardProps> = ({ 
  activeNotes, 
  startOctave = 2, 
  endOctave = 6,
  className = ""
}) => {
  const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const whiteKeys = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
  const blackKeys = ['C#', 'D#', 'F#', 'G#', 'A#'];

  // 音名をMIDI番号に変換（C4 = 60）
  const noteToMidi = (note: string): number => {
    const match = note.match(/^([A-G][#b]?)(\d+)$/);
    if (!match) return -1;
    
    const [, noteName, octaveStr] = match;
    const octave = parseInt(octaveStr);
    let noteIndex = noteNames.indexOf(noteName);
    
    // フラット記法を変換
    if (noteName.includes('b')) {
      const flatMap: { [key: string]: string } = {
        'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'
      };
      const sharpEquivalent = flatMap[noteName];
      if (sharpEquivalent) {
        noteIndex = noteNames.indexOf(sharpEquivalent);
      }
    }
    
    if (noteIndex === -1) return -1;
    return (octave + 1) * 12 + noteIndex;
  };

  // MIDI番号を音名に変換
  const midiToNote = (midi: number): { note: string; octave: number } => {
    const octave = Math.floor(midi / 12) - 1;
    const noteIndex = midi % 12;
    return { note: noteNames[noteIndex], octave };
  };

  // アクティブノートのMIDI番号セット
  const activeMidiSet = new Set(activeNotes.map(noteToMidi).filter(midi => midi !== -1));

  // 全鍵盤の配列を生成
  const generateKeys = () => {
    const keys = [];
    for (let octave = startOctave; octave <= endOctave; octave++) {
      for (let noteIndex = 0; noteIndex < 12; noteIndex++) {
        const midi = (octave + 1) * 12 + noteIndex;
        const { note } = midiToNote(midi);
        const isActive = activeMidiSet.has(midi);
        const isWhite = whiteKeys.includes(note);
        
        keys.push({
          midi,
          note,
          octave,
          fullNote: `${note}${octave}`,
          isActive,
          isWhite
        });
      }
    }
    return keys;
  };

  const keys = generateKeys();
  const whiteKeysData = keys.filter(key => key.isWhite);
  const blackKeysData = keys.filter(key => !key.isWhite);

  // 音域を最適化: オクターブ3-4のみ使用（バックエンドのボイシング設定に基づく）

  // 黒鍵の位置計算（実際の鍵盤配置に基づく）
  const getBlackKeyPosition = (note: string, octave: number) => {
    // 黒鍵がどの白鍵の間に位置するかを定義
    const blackKeyPositions: { [key: string]: { after: string } } = {
      'C#': { after: 'C' },  // C鍵の右側
      'D#': { after: 'D' },  // D鍵の右側
      'F#': { after: 'F' },  // F鍵の右側
      'G#': { after: 'G' },  // G鍵の右側
      'A#': { after: 'A' }   // A鍵の右側
    };
    
    const position = blackKeyPositions[note];
    if (!position) return 0;
    
    // 基準となる白鍵を見つける
    const baseWhiteKeyIndex = whiteKeysData.findIndex(key => 
      key.note === position.after && key.octave === octave
    );
    
    if (baseWhiteKeyIndex === -1) return 0;
    
    // 白鍵1つの幅（パーセンテージ）
    const whiteKeyWidth = 100 / whiteKeysData.length;
    
    // 黒鍵は基準白鍵の右端と次の白鍵の左端の間に配置
    // 基準白鍵の中央から右に75%程度の位置
    const blackKeyPosition = (baseWhiteKeyIndex + 0.75) * whiteKeyWidth;
    
    // 黒鍵位置の計算完了
    
    return blackKeyPosition;
  };

  return (
    <div className={`piano-keyboard relative ${className}`}>
      <div 
        className="relative h-32 bg-gray-100 rounded-lg overflow-hidden border-2 border-gray-300"
        style={{ minWidth: `${whiteKeysData.length * 25}px` }} // 白鍵1つあたり最低25px
      >
        {/* 白鍵 */}
        <div className="flex h-full w-full">
          {whiteKeysData.map((key, index) => (
            <div
              key={`white-${key.fullNote}`}
              className={`border-r border-gray-400 flex flex-col justify-end items-center pb-2 transition-colors duration-200 ${
                key.isActive 
                  ? 'bg-blue-300 border-blue-500' 
                  : 'bg-white hover:bg-gray-50'
              }`}
              style={{ 
                width: `${100 / whiteKeysData.length}%`,
                minWidth: '20px'
              }}
            >
              <span className={`text-xs font-medium select-none ${
                key.isActive ? 'text-blue-800' : 'text-gray-600'
              }`}>
                {key.note}
                <span className="text-[10px]">{key.octave}</span>
              </span>
            </div>
          ))}
        </div>

        {/* 黒鍵 */}
        {blackKeysData.map((key) => {
          const position = getBlackKeyPosition(key.note, key.octave);
          return (
            <div
              key={`black-${key.fullNote}`}
              className={`absolute top-0 rounded-b-md border border-gray-600 flex flex-col justify-end items-center pb-1 transition-colors duration-200 z-10 ${
                key.isActive 
                  ? 'bg-blue-600 border-blue-700' 
                  : 'bg-gray-800 hover:bg-gray-700'
              }`}
              style={{
                left: `${position}%`,
                width: `${(100 / whiteKeysData.length) * 0.6}%`, // 白鍵の60%の幅
                height: '80px',
                transform: 'translateX(-50%)'
              }}
            >
              <span className={`text-[8px] font-medium select-none ${
                key.isActive ? 'text-white' : 'text-gray-300'
              }`}>
                {key.note}
                <span className="text-[6px]">{key.octave}</span>
              </span>
            </div>
          );
        })}
      </div>

      {/* アクティブノート一覧 */}
      {activeNotes.length > 0 && (
        <div className="mt-2 text-sm text-gray-600">
          <span className="font-medium">構成音: </span>
          {activeNotes.join(', ')}
        </div>
      )}
    </div>
  );
};

export default PianoKeyboard;