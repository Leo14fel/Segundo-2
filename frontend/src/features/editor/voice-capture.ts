/** Microphone access only after start(); bounded recording, always release tracks. */
export class VoiceCapture {
  private recorder: MediaRecorder | null = null;
  private stream: MediaStream | null = null;
  private timer: ReturnType<typeof setTimeout> | null = null;
  private disposed = false;
  private starting = false;
  private rejected = false;
  constructor(
    private maxBytes: number,
    private maxSeconds: number,
    private onRecording: (value: boolean) => void,
    private onAudio: (audio: Blob) => void,
    private onError: (message: string) => void,
  ) {}

  async start(): Promise<void> {
    if (this.disposed || this.starting || this.recorder) return;
    if (
      typeof MediaRecorder === "undefined" ||
      !navigator.mediaDevices?.getUserMedia
    ) {
      this.onError(
        "Este navegador no permite grabar audio. Usa la aplicación en localhost o HTTPS.",
      );
      return;
    }
    this.rejected = false;
    this.starting = true;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (this.disposed) {
        stream.getTracks().forEach((track) => track.stop());
        return;
      }
      this.stream = stream;
      const mimeType = [
        "audio/webm;codecs=opus",
        "audio/ogg;codecs=opus",
        "audio/mp4",
      ].find((type) => MediaRecorder.isTypeSupported(type));
      if (!mimeType) throw new Error("UNSUPPORTED_AUDIO");
      const recorder = new MediaRecorder(stream, { mimeType });
      this.recorder = recorder;
      const chunks: Blob[] = [];
      let bytes = 0;
      recorder.ondataavailable = (event) => {
        if (this.disposed || this.rejected) return;
        bytes += event.data.size;
        if (bytes > this.maxBytes) {
          this.rejected = true;
          this.onError(
            "El audio supera el tamaño permitido. Graba una orden más corta.",
          );
          this.stop();
        } else if (event.data.size) chunks.push(event.data);
      };
      recorder.onerror = () => {
        this.rejected = true;
        if (!this.disposed) this.onError("No se pudo completar la grabación.");
        this.stop();
      };
      recorder.onstop = () => {
        this.cleanup();
        if (this.disposed) return;
        this.onRecording(false);
        if (this.rejected) return;
        const audio = new Blob(chunks, { type: recorder.mimeType || mimeType });
        if (audio.size) this.onAudio(audio);
        else this.onError("No se grabó audio. Intenta otra vez.");
      };
      recorder.start(250);
      this.onRecording(true);
      this.timer = setTimeout(() => this.stop(), this.maxSeconds * 1000);
    } catch {
      this.cleanup();
      if (!this.disposed) {
        this.onRecording(false);
        this.onError(
          "No se pudo acceder al micrófono. Revisa el permiso del navegador.",
        );
      }
    } finally {
      this.starting = false;
    }
  }
  stop(): void {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    if (this.recorder && this.recorder.state !== "inactive") {
      try {
        this.recorder.stop();
      } catch {
        this.rejected = true;
        this.cleanup();
        if (!this.disposed) {
          this.onRecording(false);
          this.onError("No se pudo detener la grabación correctamente.");
        }
      }
    } else this.cleanup();
  }
  private cleanup(): void {
    this.recorder = null;
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    this.stream?.getTracks().forEach((track) => track.stop());
    this.stream = null;
  }
  dispose(): void {
    this.disposed = true;
    this.stop();
    this.cleanup();
  }
}
