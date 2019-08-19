#!/usr/bin/python3
# from collections import namedtuple
from PyQt5 import QtCore as qc
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
import decimal
import textwrap
import minoracc as mac
import sys
from datetime import date
from logger import logger
# LMT = namedtuple('LMT', 'lmo metafora esoda ejoda')
ALIR = qc.Qt.AlignRight | qc.Qt.AlignTrailing | qc.Qt.AlignVCenter
STYLE_NORMAL = "background-color: rgb(200, 200, 200);"
STYLE_HILIGHTED = "background-color: rgb(200, 230, 200);"
STR_ACCOUNT = 'Λογαριασμός'
STR_TRANSFER = 'Μεταφορά'
STR_INCOME = 'Έσοδα'
STR_EXPENSE = 'Έξοδα'
STR_REST = 'Υπόλοιπο'
STR_TOTALS = 'Σύνολα'


def isNum(val):  # is val number or not
    """Check if val is number or not

    :param val: value to check

    :return: True if val is number else False
    """
    try:
        float(val)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """Returns a decimal. If poso is not a number or None returns dec(0)

    :param poso: the number to transofrm to decimal
    :param decimals: Number of decimals

    :return: A decimal number with specific number of decimal digits
    """
    poso = 0 if (poso is None) else poso
    tmp = decimal.Decimal(poso) if isNum(poso) else decimal.Decimal('0')
    tmp = decimal.Decimal(0) if decimal.Decimal(0) else tmp
    return tmp.quantize(decimal.Decimal(10) ** (-1 * decimals))


def triades(txt, separator='.'):
    """Help function to split digits to thousants (123456 becomes 123.456)

    :param txt: text to split
    :param separator: The separator to use

    :return: txt separated by separator in group of three

    Example::

        >>> import gr
        >>> gr.triades('abcdefg')
        'a.bcd.efg'
        >>> gr.triades('abcdefg', separator='|')
        'a|bcd|efg'
    """
    return separator.join(textwrap.wrap(txt[::-1], 3))[::-1]


def dec2gr(poso, decimals=2, zero_as_space=False):
    """Returns string formatted as Greek decimal (1234.56 becomes 1.234,56)

    :param poso: number to format
    :param decimals: Number of decimal digits
    :param zero_as_space: if True then zero values become one space

    :return: Greek formatted number

    Example::

        >>> import gr
        >>> gr.dec2gr('-2456')
        '-2.456,00'
        >>> gr.dec2gr(0, zero_as_space=True)
        ' '
    """
    dposo = dec(poso, decimals)
    if dposo == dec(0):
        if zero_as_space:
            return ' '
        else:
            return '0'
    sdposo = str(dposo)
    meion = '-'
    decimal_ceparator = ','
    prosimo = ''
    if sdposo.startswith(meion):
        prosimo = meion
        sdposo = sdposo.replace(meion, '')
    if '.' in sdposo:
        sint, sdec = sdposo.split('.')
    else:
        sint = sdposo
        decimal_ceparator = ''
        sdec = ''
    return prosimo + ' ' + triades(sint) + decimal_ceparator + sdec


class AccountWidget(qw.QWidget):
    acc_clicked = qc.pyqtSignal(str)

    def __init__(self, lmos, metafora, esoda, ejoda, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLE_NORMAL)
        self.setMouseTracking(True)
        self._create_fonts(10)
        self._create_ui()
        # if lmos.startswith('ταμείο.'):
        #     lmos = lmos.replace('ταμείο.', '')
        self.set_vals(lmos, metafora, esoda, ejoda)

    def _create_fonts(self, size=12):
        self.bfont = qg.QFont()
        self.bfont.setPointSize(size)
        self.bfont.setBold(True)
        self.bfont.setWeight(75)
        self.font = qg.QFont()
        self.font.setPointSize(size)

    def set_vals(self, lmos, meta, eso, ejo):
        self.lmos = lmos
        self.meta = dec(meta)
        self.eso = dec(eso)
        self.ejo = dec(ejo)
        self.ypo = self.meta + self.eso + self.ejo
        self.logariasmos.setText(lmos)
        self.metafora.setText(dec2gr(self.meta))  # '%12.2f' % meta)
        self.esoda.setText(dec2gr(self.eso))  # '%12.2f' % eso)
        self.ejoda.setText(dec2gr(self.ejo))  # '%12.2f' % (ejo))
        # ypo = meta + eso + ejo
        self.ypoloipo.setText(dec2gr(self.ypo))  # '%12.2f' % self.ypo)

    def vals(self):
        return (self.lmos, self.meta, self.eso, self.ejo, self.ypo)

    def __str__(self):
        return "%s %s %s %s %s" % self.vals()

    def mousePressEvent(self, ev):
        # qw.QMessageBox.information(self, 'Title Ted', 'lmos: %s' % self)
        self.acc_clicked.emit(self.lmos)
        return qw.QWidget.mousePressEvent(self, ev)

    def enterEvent(self, ev):
        self.setStyleSheet(STYLE_HILIGHTED)
        return qw.QWidget.enterEvent(self, ev)

    def leaveEvent(self, ev):
        self.setStyleSheet(STYLE_NORMAL)
        return qw.QWidget.leaveEvent(self, ev)

    def _create_ui(self):
        mainlayout = qw.QVBoxLayout(self)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        self.logariasmos = qw.QLabel(STR_ACCOUNT)
        self.logariasmos.setFont(self.bfont)
        mainlayout.addWidget(self.logariasmos)
        layout = qw.QFormLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(1)
        mainlayout.addLayout(layout)
        lmetafora = qw.QLabel(STR_TRANSFER)
        lmetafora.setFont(self.font)
        lesoda = qw.QLabel(STR_INCOME)
        lesoda.setFont(self.font)
        lejoda = qw.QLabel(STR_EXPENSE)
        lejoda.setFont(self.font)
        lypoloipo = qw.QLabel(STR_REST)
        lypoloipo.setFont(self.font)
        line = qw.QFrame()
        line.setFrameShadow(qw.QFrame.Plain)
        line.setLineWidth(3)
        line.setFrameShape(qw.QFrame.HLine)
        self.metafora = qw.QLabel('0,00')
        self.metafora.setFont(self.font)
        self.esoda = qw.QLabel('0,00')
        self.esoda.setFont(self.font)
        self.ejoda = qw.QLabel('0,00')
        self.ejoda.setFont(self.font)
        self.ypoloipo = qw.QLabel('0,00')
        self.ypoloipo.setFont(self.font)
        # alignement
        self.logariasmos.setAlignment(qc.Qt.AlignCenter)
        self.metafora.setAlignment(ALIR)
        self.esoda.setAlignment(ALIR)
        self.ejoda.setAlignment(ALIR)
        self.ypoloipo.setAlignment(ALIR)
        # add to layout manager
        layout.setWidget(0, qw.QFormLayout.LabelRole, lmetafora)
        layout.setWidget(0, qw.QFormLayout.FieldRole, self.metafora)
        layout.setWidget(1, qw.QFormLayout.LabelRole, lesoda)
        layout.setWidget(1, qw.QFormLayout.FieldRole, self.esoda)
        layout.setWidget(2, qw.QFormLayout.LabelRole, lejoda)
        layout.setWidget(2, qw.QFormLayout.FieldRole, self.ejoda)
        layout.setWidget(3, qw.QFormLayout.FieldRole, line)
        layout.setWidget(4, qw.QFormLayout.LabelRole, lypoloipo)
        layout.setWidget(4, qw.QFormLayout.FieldRole, self.ypoloipo)


class SideBar(qw.QWidget):
    some_acc_clicked = qc.pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        laym = qw.QVBoxLayout(self)
        scroll = qw.QScrollArea(self)
        scroll.setWidgetResizable(True)
        laym.addWidget(scroll)
        scont = qw.QWidget()
        lay = qw.QVBoxLayout(scont)
        self.layn = qw.QVBoxLayout()
        lay.addLayout(self.layn)
        self.totals = AccountWidget(STR_TOTALS, 0, 0, 0)
        lay.addWidget(self.totals)
        spacer = qw.QSpacerItem(20, 20, qw.QSizePolicy.Minimum,
                                qw.QSizePolicy.Expanding)
        lay.addItem(spacer)
        scroll.setWidget(scont)
        self.accounts = {}
        self.setMaximumWidth(300)
        self.setMinimumWidth(300)

    def add(self, lmos, met, eso, ejo):
        tlmos, tmet, teso, tejo, _ = self.totals.vals()
        tmet += dec(met)
        teso += dec(eso)
        tejo += dec(ejo)
        if lmos in self.accounts:
            self.accounts[lmos].set_vals(lmos, met, eso, ejo)
        else:
            self.accounts[lmos] = AccountWidget(lmos, met, eso, ejo, self)
            self.layn.addWidget(self.accounts[lmos])
            self.accounts[lmos].acc_clicked.connect(self.some_clicked)
        self.totals.set_vals(tlmos, tmet, teso, tejo)

    def some_clicked(self, val):
        # qw.QMessageBox.information(self, 'Title  fgdfg Ted', 'lmos: %s' % val)
        self.some_acc_clicked.emit(val)

    def add_many(self, lmoi):
        '''lmoi: tuple'''
        lmoi.sort()
        for lmo in lmoi:
            if dec(lmo[1] + lmo[2] + lmo[3]) != 0:
                self.add(*lmo)


class Dmodel(qc.QAbstractTableModel):
    """We pass a dictionary of values as data source"""
    def __init__(self, imodel, parent=None):
        super().__init__(parent)
        self.set_data(imodel)

    def set_data(self, model_data):
        self.headers, self.vals, self.align, self.typos = model_data

    def rowCount(self, parent):
        return len(self.vals)

    def columnCount(self, parent):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if role == qc.Qt.DisplayRole:
            if orientation == qc.Qt.Horizontal:
                return self.headers[section]
            else:
                pass
                # return section + 1
        if role == qc.Qt.TextAlignmentRole:
            return qc.Qt.AlignCenter

    # def index(self, row, column, parent):
    #     return qc.QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == qc.Qt.DisplayRole:
            if self.typos[index.column()] == 1:
                return  dec2gr(self.vals[index.row()][index.column()])
            else:
                return self.vals[index.row()][index.column()]
        if role == qc.Qt.TextAlignmentRole:
            if self.align[index.column()] == 1:
                return qc.Qt.AlignLeft
            elif self.align[index.column()] == 2:
                return qc.Qt.AlignCenter
            elif self.align[index.column()] == 3:
                return qc.Qt.AlignRight


class Dialog(qw.QWidget):
    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.book = mac.Book.from_file(filename, '2030-10-31')
        mainlayout = qw.QVBoxLayout()
        self.setLayout(mainlayout)
        hlayout = qw.QHBoxLayout()
        mainlayout.addLayout(hlayout)
        leftv = qw.QVBoxLayout()
        rightv = qw.QSplitter()
        rightv.setOrientation(qc.Qt.Vertical)
        hlayout.addLayout(leftv)
        hlayout.addWidget(rightv)
        self.sbar = SideBar(self)
        self.sbar.add_many(self.book.tamiaka2list())
        leftv.addWidget(self.sbar)
        bsave_ypol = qw.QPushButton("Μεταφορά υπολοίπων")
        leftv.addWidget(bsave_ypol)
        self.iso = qw.QTableView(rightv)
        self.iso.setModel(Dmodel(self.book.isozygio_model()))
        self.iso.resizeColumnsToContents()
        self.tbl = qw.QTableView(rightv)
        self.tbl.setWordWrap(True)
        self.setWindowTitle("Ισοζύγιο Λογαριασμών")
        if self.parent:
            self.parent.setWindowTitle("Ισοζύγιο Λογαριασμών")
        # Connections
        bsave_ypol.clicked.connect(self.save_ypol)
        self.sbar.some_acc_clicked.connect(self.refresh_model)
        self.iso.clicked.connect(self.refresh_model_from_iso)
        self.tbl.doubleClicked.connect(self.model_rowdata)

    def model_rowdata(self, idx):
        tran = self.book.trans[self.model_lmos.vals[idx.row()][0]]
        stv = "Ημερομηνία: {dat}\nΑπό : {apo}\nΣε  : {se}\nΠοσό: {val}\nΠεριγραφή: {per}"
        qw.QMessageBox.information(self,
                                   "Εγγραφή %s" % (tran.row_dict['id']),
                                   stv.format(**tran.row_dict))

    def save_ypol(self):
        fname, _ = qw.QFileDialog.getSaveFileName(self, 'Filename', 'ypol', '')
        if fname:
            self.book.metafora_ypoloipon(date.today().isoformat(), fname)

    def refresh_model_from_iso(self, acc):
        if acc.column() == 0:
            self.refresh_model(acc.data())

    def refresh_model(self, lmos):
        self.setWindowTitle("%s" % lmos)
        if self.parent:
            self.parent.setWindowTitle("%s" % lmos)
        self.model_lmos = Dmodel(self.book.kartella_model(lmos))
        self.tbl.setModel(self.model_lmos)
        self.tbl.setColumnWidth(0, 50)
        self.tbl.setColumnWidth(1, 100)
        self.tbl.setColumnWidth(2, 450)
        self.tbl.resizeRowsToContents()


def test_sidebar(lmoi):
    app = qw.QApplication(sys.argv)
    sbar = SideBar()
    sbar.add_many(lmoi)
    sbar.show()
    sys.exit(app.exec_())


def test_app(filename):
    app = qw.QApplication(sys.argv)
    dlg = Dialog(filename)
    dlg.show()
    sys.exit(app.exec_())


class MainWindow(qw.QMainWindow):
    def __init__(self, filename=None):
        super().__init__()
        self.setAttribute(qc.Qt.WA_DeleteOnClose)
        self.settings = qc.QSettings()
        self.setMinimumSize(1250, 800)
        # self.isUntitled = True
        self.fnam = filename
        self.createMenus()
        if self.fnam:
            self.init_vals(self.fnam)
        else:
            self.fnam = self.settings.value("filename", defaultValue=None)
            if self.fnam:
                self.init_vals(self.fnam)


    def init_vals(self, filename):
        self.dlg = Dialog(filename, self)
        self.setCentralWidget(self.dlg)

    def createMenus(self):
        self.openAct = qw.QAction(
            'Open',
            self,
            statusTip='Open file',
            triggered=self.open)
        self.filemenu = self.menuBar().addMenu("&File")
        self.filemenu.addAction(self.openAct)

    def open(self):
        fnam, _ = qw.QFileDialog.getOpenFileName(self, 'Open', self.fnam, '')
        if fnam:
            self.init_vals(fnam)
            self.settings.setValue("filename", fnam)


def main(filename=None):
    app = qw.QApplication(sys.argv)
    app.setOrganizationName("TedLazaros")
    app.setOrganizationDomain("Tedlaz")
    app.setApplicationName("MinorAccounting")
    dlg = MainWindow(filename)
    dlg.show()
    logger.info("Application started !!!")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
