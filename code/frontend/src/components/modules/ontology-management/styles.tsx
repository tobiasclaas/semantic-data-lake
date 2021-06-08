import Grid from "@material-ui/core/Grid";
import { withStyles } from "@material-ui/core/styles";

export const ContainerGrid = withStyles(() => ({
  root: {
    marginTop: "1rem",
  },
}))(Grid);
