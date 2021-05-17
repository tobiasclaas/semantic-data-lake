import { createMuiTheme } from "@material-ui/core/styles";
import blue from '@material-ui/core/colors/blue';

const theme = createMuiTheme({
    palette: {
        primary: {
            main: blue[500]

        }
    }
})

theme.overrides = {
    ...theme.overrides,
    MuiCssBaseline: {
        '@global': {
            body: {
                backgroundColor: '#f1f1f1',
            },
            '.no-highlight': {
                WebkitTouchCallout: 'none',
                WebkitUserSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                userSelect: 'none'
            }
        }
    },
    MuiButton: {
        label: {
            pointerEvents: 'none',
            textTransform: 'none'
        }
    },
    MuiTypography: {
        root: {
            WebkitTouchCallout: 'none',
            WebkitUserSelect: 'none',
            MozUserSelect: 'none',
            msUserSelect: 'none',
            userSelect: 'none'
        },
        subtitle1: {
            fontSize: theme.typography.pxToRem(18),
            color: 'rgba(0, 0, 0, 0.6)'
        }
    },
    MuiTabs: {
        indicator: {
            background: theme.palette.primary.contrastText
        }
    },
    MuiTab: {
        root: {
            textTransform: 'none'
        }
    }
}

export default theme