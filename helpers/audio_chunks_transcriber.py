import os

from helpers.load_torch_audio import load_audio


def transcribe_chunks(chunks_dir: str, model, processor, language="english"):
    print("\nStarted transcribing...")
    transcriptions = []
    for file in sorted(os.listdir(chunks_dir)):
        if not file.endswith(".wav"):
            continue
        chunk_path = os.path.join(chunks_dir, file)

        # load audio with processor
        speech = load_audio(chunk_path)  # if you have your own loader use it
        input_features = processor(
            speech, return_tensors="pt", sampling_rate=16000
        ).input_features.to(model.device)

        forced_decoder_ids = processor.get_decoder_prompt_ids(
            language=language, task="transcribe"
        )
        predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        transcriptions.append(transcription.strip())
        print(f"Processed {len(transcriptions)} chunk(s)")

    return " ".join(transcriptions)
