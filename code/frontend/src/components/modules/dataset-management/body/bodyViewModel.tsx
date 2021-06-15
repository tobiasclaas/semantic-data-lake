import ContentStore from "../../../../models/contentStore";

abstract class BodyViewModel extends ContentStore {
  abstract canUpload(): boolean;
}

export default BodyViewModel;
