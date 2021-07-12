import Fab from "@material-ui/core/Fab";
import { withStyles } from "@material-ui/core/styles";

const TopRightSecondFab = withStyles({
  root: {
    position: "absolute",
    top: 60,
    right: 0,
  },
})(Fab);

export default TopRightSecondFab;
