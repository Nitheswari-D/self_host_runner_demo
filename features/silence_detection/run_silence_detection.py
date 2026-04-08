import os
from datetime import datetime

from features.silence_detection.mic_test import mic_test
from features.silence_detection.split_audio import split_audio
from features.silence_detection.analyze_silence import analyze_silence



def run_silence_detection(mic_name,mic_index, base_dir, duration, chunk_duration, playback_file, playback_device, playback_device_index):
    try:
        # Create base directory if not exists
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # File naming
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_filename = f"recording_{timestamp}"

        full_filename = os.path.join(base_dir, f"{base_filename}.wav")
        split_folder = os.path.join(base_dir, f"{base_filename}_split_audio")
        report_filename = os.path.join(base_dir, f"{base_filename}_silence_report.txt")

        # Record audio
        print("\n Starting recording...")
        mic_test(device_name=mic_name, device_index=mic_index, filename=full_filename, duration=duration, playback_file=playback_file, playback_device=playback_device, playback_device_index=playback_device_index)

        # Validate recording
        if not os.path.exists(full_filename):
            raise Exception("Recording failed: file not created")

        print("Recording completed")

        # Split audio
        print("\nSplitting audio...")
        chunk_files = split_audio(full_filename, chunk_duration, split_folder, base_filename)

        # Validate splitting
        if not chunk_files:
            raise Exception("Splitting failed: no chunks created")

        print(f"{len(chunk_files)} chunks created")

        # Analyze silence
        print("\n Analyzing silence...")
        with open(report_filename, 'w') as report_file:

            for idx, chunk_path in enumerate(chunk_files, 1):
                chunk_name = os.path.basename(chunk_path)

                print(f"\nAnalyzing chunk {idx} ({chunk_name}):")
                report_file.write(f"--- Silence in chunk {idx} ({chunk_name}) ---\n")

                silences = analyze_silence(chunk_path)

                if silences:
                    for start_ms, end_ms in silences:
                        text = f"Silence from {start_ms/1000:.2f}s to {end_ms/1000:.2f}s"
                        print(text)
                        report_file.write(text + "\n")
                else:
                    print("No significant silence detected.")
                    report_file.write("No significant silence detected.\n")

                report_file.write("\n")

        print(f"\n Silence report saved: {report_filename}")

        return True  

    except Exception as e:
        print(f"\n Error in silence detection: {e}")
        return False  