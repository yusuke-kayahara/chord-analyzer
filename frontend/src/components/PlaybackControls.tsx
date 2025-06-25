import React, { useState, useEffect, useRef } from 'react';
import * as Tone from 'tone';
import { AnalysisResponse } from '../types/chord';

interface PlaybackControlsProps {
  analysisResult: AnalysisResponse;
}

const PlaybackControls: React.FC<PlaybackControlsProps> = ({ analysisResult }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const synth = useRef<Tone.PolySynth | null>(null);

  // エレクトリックピアノ風の音色を作成
  useEffect(() => {
    synth.current = new Tone.PolySynth(Tone.FMSynth, {
      harmonicity: 3.01,
      modulationIndex: 14,
      envelope: {
        attack: 0.01,
        decay: 0.1,
        sustain: 0.1,
        release: 0.8,
      },
      modulation: {
        type: 'sine',
      },
      modulationEnvelope: {
        attack: 0.02,
        decay: 0.2,
        sustain: 0.0,
        release: 0.5,
      },
    }).toDestination();

    return () => {
      synth.current?.dispose();
    };
  }, []);

  const handlePlay = async () => {
    if (isPlaying) {
      Tone.Transport.stop();
      setIsPlaying(false);
      return;
    }

    if (Tone.context.state !== 'running') {
      await Tone.start();
    }

    const notesToPlay = analysisResult.progression_details.map(detail => {
      // 音名をオクターブ付きに変換 (例: C -> C4)
      return detail.components.map(note => `${note}4`);
    });

    const sequence = new Tone.Sequence((time, notes) => {
      synth.current?.triggerAttackRelease(notes, '1n', time);
    }, notesToPlay, '1n').start(0);

    Tone.Transport.start();
    setIsPlaying(true);

    Tone.Transport.on('stop', () => {
      setIsPlaying(false);
      sequence.dispose();
    });
  };

  return (
    <div className="flex justify-center my-4">
      <button
        onClick={handlePlay}
        className={`px-6 py-3 text-white font-bold rounded-lg shadow-md transition-transform transform hover:scale-105 ${
          isPlaying ? 'bg-red-500' : 'bg-blue-500'
        }`}>
        {isPlaying ? '停止' : '進行を再生'}
      </button>
    </div>
  );
};

export default PlaybackControls;
