import { withStyles } from "@material-ui/core/styles"
import Backdrop from "@material-ui/core/Backdrop"
import DialogTitle from "@material-ui/core/DialogTitle"

// profile modal
export const StyledBackdrop = withStyles(() => ({
    root: {
        position: "absolute",
        zIndex: 1,
        backgroundColor: "rgba(255,255,255,0.25)"
    }
}))(Backdrop)

export const PadlessDialogTitle = withStyles(() => ({
    root: {
        padding: 0
    }
}))(DialogTitle)
