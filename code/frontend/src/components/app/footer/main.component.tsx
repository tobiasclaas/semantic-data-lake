import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import { useTheme } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import React from 'react';
import rwth from '../../../resources/images/rwth-aachen.png'
import fraunhofer from '../../../resources/images/fraunhofer.svg'

const Footer: React.FC = () => {
    const theme = useTheme()

    return (
        <div
            className='no-highlight'
            style={{
                backgroundColor: theme.palette.primary.main,
                color: theme.palette.primary.contrastText,
                overflow: 'unset',
                pointerEvents: 'none'
            }}
        >
            <Container style={{ marginTop: '2rem', marginBottom: '2rem' }}>
                <Grid
                    container
                    justify='space-between'

                >
                    <Grid item style={{ marginRight: '3rem' }}>
                        <Typography variant='h6'>Data Lake App</Typography>
                        <Typography variant='body2' style={{ marginTop: '0.5rem' }}>Semantic Data Integration (Lab)</Typography>
                        <Typography variant='body2'>Summer Semester 2021</Typography>
                    </Grid>

                    <Grid
                        item
                        container
                        wrap='nowrap'
                        style={{
                            marginRight: '3rem',
                            width: '24%'
                        }}
                        spacing={3}
                        alignItems='stretch'
                    >
                        <Grid item xs>
                            <img src={rwth} style={{ height: '100%', width: '100%', objectFit: 'contain', objectPosition: 'bottom' }} />
                        </Grid>
                        <Grid item xs>
                            <img src={fraunhofer} style={{ height: '100%', width: '100%', objectFit: 'contain', objectPosition: 'bottom' }} />
                        </Grid>
                    </Grid>
                </Grid>

            </Container>
        </div>
    );
}

export default Footer