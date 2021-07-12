import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import TopRightFab from "../../../common/topRightFab";
import AddIcon from "@material-ui/icons/Add";
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogContent from "@material-ui/core/DialogContent";
import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import { ContainerGrid } from "../styles";
import FileInput from "../../../common/FileInput";
import Item from "../../../common/item";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import InputLabel from "@material-ui/core/InputLabel";
import FormControl from "@material-ui/core/FormControl";
import Grid from "@material-ui/core/Grid";
import LocalOfferIcon from "@material-ui/icons/LocalOffer";
import ItemButton from "../../../common/item/button";
import { blue } from "@material-ui/core/colors";
import TableContainer from "@material-ui/core/TableContainer";
import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import { withStyles, makeStyles } from '@material-ui/core/styles';

const StyledTableCell = withStyles((theme) => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

const StyledTableRow = withStyles((theme) => ({
  root: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);


const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  return (
    <React.Fragment>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              {
                viewModel.headers.map((item, index) => (
                  <StyledTableCell key={item}>
                    {item}
                  </StyledTableCell>
                ))
              }
              {/*<TableCell align="right">Uri</TableCell>*/}
            </TableRow>
          </TableHead>
          <TableBody>
            {viewModel.data.map((row, index) => (
                <StyledTableRow key={index}>
                  {
                    row.map((data,index) => (
                      <TableCell key={index} component="th" scope="row">
                        {data}
                      </TableCell>
                    ))
                  }
                </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </React.Fragment>
  );
});

export default Main;
