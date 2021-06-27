import ContentStore from "../../../../models/contentStore";

abstract class BodyViewModel extends ContentStore {
  abstract canUpload(): boolean;
  abstract fill(formData: FormData): void;
}

export default BodyViewModel;
