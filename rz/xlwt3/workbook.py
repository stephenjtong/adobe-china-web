from . import biffrecords
from . import style
from . import compounddoc
from . import utils
from .worksheet import Worksheet

class Workbook(object):
    """ The main Excel file object. """
    def __init__(self, encoding='ascii', style_compression=0):
        self.encoding = encoding
        self.__owner = 'None'
        self.__country_code = None # 0x07 is Russia :-)
        self.__wnd_protect = 0
        self.__obj_protect = 0
        self.__protect = 0
        self.__backup_on_save = 0
        # for WINDOW1 record
        self.__hpos_twips = 0x01E0
        self.__vpos_twips = 0x005A
        self.__width_twips = 0x3FCF
        self.__height_twips = 0x2A4E

        self.__active_sheet = 0
        self.__first_tab_index = 0
        self.__selected_tabs = 0x01
        self.__tab_width_twips = 0x0258

        self.__wnd_hidden = 0
        self.__wnd_mini = 0
        self.__hscroll_visible = 1
        self.__vscroll_visible = 1
        self.__tabs_visible = 1

        self.__styles = style.StyleCollection(style_compression)

        self.__dates_1904 = 0
        self.__use_cell_values = 1

        self.__sst = biffrecords.SharedStringTable(self.encoding)

        self.__worksheets = []
        self.__worksheet_idx_from_name = {}
        self.__sheet_refs = {}
        self._supbook_xref = {}
        self._xcall_xref = {}
        self._ownbook_supbookx = None
        self._ownbook_supbook_ref = None
        self._xcall_supbookx = None
        self._xcall_supbook_ref = None

    def get_style_stats(self):
        return self.__styles.stats[:]

    # owner property
    def set_owner(self, value):
        self.__owner = value
    def get_owner(self):
        return self.__owner
    owner = property(get_owner, set_owner)

    # county code property
    def set_country_code(self, value):
        self.__country_code = value
    def get_country_code(self):
        return self.__country_code
    country_code = property(get_country_code, set_country_code)

    # wnd_protect property
    def set_wnd_protect(self, value):
        self.__wnd_protect = int(value)
    def get_wnd_protect(self):
        return bool(self.__wnd_protect)
    wnd_protect = property(get_wnd_protect, set_wnd_protect)

    # obj_protect property
    def set_obj_protect(self, value):
        self.__obj_protect = int(value)
    def get_obj_protect(self):
        return bool(self.__obj_protect)
    obj_protect = property(get_obj_protect, set_obj_protect)

    # protect property
    def set_protect(self, value):
        self.__protect = int(value)
    def get_protect(self):
        return bool(self.__protect)
    protect = property(get_protect, set_protect)

    # backup_on_save property
    def set_backup_on_save(self, value):
        self.__backup_on_save = int(value)
    def get_backup_on_save(self):
        return bool(self.__backup_on_save)
    backup_on_save = property(get_backup_on_save, set_backup_on_save)

    # hpos property
    def set_hpos(self, value):
        self.__hpos_twips = value & 0xFFFF
    def get_hpos(self):
        return self.__hpos_twips
    hpos = property(get_hpos, set_hpos)

    # vpos property
    def set_vpos(self, value):
        self.__vpos_twips = value & 0xFFFF
    def get_vpos(self):
        return self.__vpos_twips
    vpos = property(get_vpos, set_vpos)

    # width property
    def set_width(self, value):
        self.__width_twips = value & 0xFFFF
    def get_width(self):
        return self.__width_twips
    width = property(get_width, set_width)

    # height property
    def set_height(self, value):
        self.__height_twips = value & 0xFFFF
    def get_height(self):
        return self.__height_twips
    height = property(get_height, set_height)

    # active_sheet propterty
    def set_active_sheet(self, value):
        self.__active_sheet = value & 0xFFFF
        self.__first_tab_index = self.__active_sheet
    def get_active_sheet(self):
        return self.__active_sheet
    active_sheet = property(get_active_sheet, set_active_sheet)

    # tab_width property
    def set_tab_width(self, value):
        self.__tab_width_twips = value & 0xFFFF
    def get_tab_width(self):
        return self.__tab_width_twips
    tab_width = property(get_tab_width, set_tab_width)

    # wnd_visible property
    def set_wnd_visible(self, value):
        self.__wnd_hidden = int(not value)
    def get_wnd_visible(self):
        return not bool(self.__wnd_hidden)
    wnd_visible = property(get_wnd_visible, set_wnd_visible)

    # wnd_mini property
    def set_wnd_mini(self, value):
        self.__wnd_mini = int(value)
    def get_wnd_mini(self):
        return bool(self.__wnd_mini)
    wnd_mini = property(get_wnd_mini, set_wnd_mini)

    # hscroll_visible property
    def set_hscroll_visible(self, value):
        self.__hscroll_visible = int(value)
    def get_hscroll_visible(self):
        return bool(self.__hscroll_visible)
    hscroll_visible = property(get_hscroll_visible, set_hscroll_visible)

    # vscroll_visible property
    def set_vscroll_visible(self, value):
        self.__vscroll_visible = int(value)
    def get_vscroll_visible(self):
        return bool(self.__vscroll_visible)
    vscroll_visible = property(get_vscroll_visible, set_vscroll_visible)

    # tabs_visible property
    def set_tabs_visible(self, value):
        self.__tabs_visible = int(value)
    def get_tabs_visible(self):
        return bool(self.__tabs_visible)
    tabs_visible = property(get_tabs_visible, set_tabs_visible)

    # dates_1904 property
    def set_dates_1904(self, value):
        self.__dates_1904 = int(value)
    def get_dates_1904(self):
        return bool(self.__dates_1904)
    dates_1904 = property(get_dates_1904, set_dates_1904)

    # use_cell_values property
    def set_use_cell_values(self, value):
        self.__use_cell_values = int(value)
    def get_use_cell_values(self):
        return bool(self.__use_cell_values)
    use_cell_values = property(get_use_cell_values, set_use_cell_values)

    # default_style property
    def get_default_style(self):
        return self.__styles.default_style
    default_style = property(get_default_style)

    def add_sheet(self, sheetname, cell_overwrite_ok=False):
        """ Add a new Worksheet 'sheetname'.
        """
        # API method
        if not isinstance(sheetname, str):
            sheetname = sheetname.decode(self.encoding)

        if not utils.valid_sheet_name(sheetname):
            raise Exception("invalid worksheet name %r" % sheetname)

        lower_name = sheetname.lower()
        if lower_name in self.__worksheet_idx_from_name:
            raise Exception("duplicate worksheet name %r" % sheetname)

        self.__worksheet_idx_from_name[lower_name] = len(self.__worksheets)
        self.__worksheets.append(Worksheet(sheetname, self, cell_overwrite_ok))
        return self.__worksheets[-1]

    def save(self, filename):
        """ Save Workbook (xls-file) to 'filename'.
        """
        # API method
        doc = compounddoc.XlsDoc()
        doc.save(filename, self.get_biff_data())

    def get_sheet(self, sheetnum):
        # API method
        return self.__worksheets[sheetnum]

    def raise_bad_sheetname(self, sheetname):
        raise Exception("Formula: unknown sheet name %s" % sheetname)

    def convert_sheetindex(self, strg_ref, n_sheets):
        idx = int(strg_ref)
        if 0 <= idx < n_sheets:
            return idx
        msg = "Formula: sheet index (%s) >= number of sheets (%d)" % (strg_ref, n_sheets)
        raise Exception(msg)

    def add_style(self, style):
        return self.__styles.add(style)

    def add_str(self, s):
        return self.__sst.add_str(s)

    def del_str(self, sst_idx):
        self.__sst.del_str(sst_idx)

    def str_index(self, s):
        return self.__sst.str_index(s)

    def _get_supbook_index(self, tag):
        if tag in self._supbook_xref:
            return self._supbook_xref[tag]
        self._supbook_xref[tag] = idx = len(self._supbook_xref)
        return idx

    def setup_ownbook(self):
        self._ownbook_supbookx = self._get_supbook_index(('ownbook', 0))
        self._ownbook_supbook_ref = None
        reference = (self._ownbook_supbookx, 0xFFFE, 0xFFFE)
        if reference in self.__sheet_refs:
            raise Exception("can't happen")
        self.__sheet_refs[reference] = self._ownbook_supbook_ref = len(self.__sheet_refs)

    def setup_xcall(self):
        self._xcall_supbookx = self._get_supbook_index(('xcall', 0))
        self._xcall_supbook_ref = None
        reference = (self._xcall_supbookx, 0xFFFE, 0xFFFE)
        if reference in self.__sheet_refs:
            raise Exception("can't happen")
        self.__sheet_refs[reference] = self._xcall_supbook_ref = len(self.__sheet_refs)

    def add_sheet_reference(self, formula):
        # seems not to be an API method -- called by Worksheet.write()
        # formula -- an ExcelFormula.Formula() object

        patches = []
        n_sheets = len(self.__worksheets)
        sheet_refs, xcall_refs = formula.get_references()

        for ref0, ref1, offset in sheet_refs:
            if not ref0.isdigit():
                try:
                    ref0n = self.__worksheet_idx_from_name[ref0.lower()]
                except KeyError:
                    self.raise_bad_sheetname(ref0)
            else:
                ref0n = self.convert_sheetindex(ref0, n_sheets)
            if ref1 == ref0:
                ref1n = ref0n
            elif not ref1.isdigit():
                try:
                    ref1n = self.__worksheet_idx_from_name[ref1.lower()]
                except KeyError:
                    self.raise_bad_sheetname(ref1)
            else:
                ref1n = self.convert_sheetindex(ref1, n_sheets)
            if ref1n < ref0n:
                msg = "Formula: sheets out of order; %r:%r -> (%d, %d)" \
                    % (ref0, ref1, ref0n, ref1n)
                raise Exception(msg)
            if self._ownbook_supbookx is None:
                self.setup_ownbook()
            reference = (self._ownbook_supbookx, ref0n, ref1n)
            if reference in self.__sheet_refs:
                patches.append((offset, self.__sheet_refs[reference]))
            else:
                nrefs = len(self.__sheet_refs)
                if nrefs > 65535:
                    raise Exception('More than 65536 inter-sheet references')
                self.__sheet_refs[reference] = nrefs
                patches.append((offset, nrefs))

        for funcname, offset in xcall_refs:
            if self._ownbook_supbookx is None:
                self.setup_ownbook()
            if self._xcall_supbookx is None:
                self.setup_xcall()

            patches.append((offset, self._xcall_supbook_ref))
            if not isinstance(funcname, str):
                funcname = funcname.decode(self.encoding)
            if funcname in self._xcall_xref:
                idx = self._xcall_xref[funcname]
            else:
                self._xcall_xref[funcname] = idx = len(self._xcall_xref)
            patches.append((offset + 2, idx + 1))

        formula.patch_references(patches)

    def _tobytes(self, string):
        return bytes(string, self.encoding)

    ##################################################################
    ## BIFF records generation
    ##################################################################

    def __bof_rec(self):
        return biffrecords.Biff8BOFRecord(biffrecords.Biff8BOFRecord.BOOK_GLOBAL).get()

    def __eof_rec(self):
        return biffrecords.EOFRecord().get()

    def __intf_hdr_rec(self):
        return biffrecords.InteraceHdrRecord().get()

    def __intf_end_rec(self):
        return biffrecords.InteraceEndRecord().get()

    def __intf_mms_rec(self):
        return biffrecords.MMSRecord().get()

    def __write_access_rec(self):
        owner = self._tobytes(self.__owner)
        return biffrecords.WriteAccessRecord(owner).get()

    def __wnd_protect_rec(self):
        return biffrecords.WindowProtectRecord(self.__wnd_protect).get()

    def __obj_protect_rec(self):
        return biffrecords.ObjectProtectRecord(self.__obj_protect).get()

    def __protect_rec(self):
        return biffrecords.ProtectRecord(self.__protect).get()

    def __password_rec(self):
        return biffrecords.PasswordRecord().get()

    def __prot4rev_rec(self):
        return biffrecords.Prot4RevRecord().get()

    def __prot4rev_pass_rec(self):
        return biffrecords.Prot4RevPassRecord().get()

    def __backup_rec(self):
        return biffrecords.BackupRecord(self.__backup_on_save).get()

    def __hide_obj_rec(self):
        return biffrecords.HideObjRecord().get()

    def __window1_rec(self):
        flags = 0
        flags |= (self.__wnd_hidden) << 0
        flags |= (self.__wnd_mini) << 1
        flags |= (self.__hscroll_visible) << 3
        flags |= (self.__vscroll_visible) << 4
        flags |= (self.__tabs_visible) << 5

        return biffrecords.Window1Record(self.__hpos_twips, self.__vpos_twips,
                                self.__width_twips, self.__height_twips,
                                flags,
                                self.__active_sheet, self.__first_tab_index,
                                self.__selected_tabs, self.__tab_width_twips).get()

    def __codepage_rec(self):
        return biffrecords.CodepageBiff8Record().get()

    def __country_rec(self):
        if not self.__country_code:
            return b''
        return biffrecords.CountryRecord(self.__country_code, self.__country_code).get()

    def __dsf_rec(self):
        return biffrecords.DSFRecord().get()

    def __tabid_rec(self):
        return biffrecords.TabIDRecord(len(self.__worksheets)).get()

    def __fngroupcount_rec(self):
        return biffrecords.FnGroupCountRecord().get()

    def __datemode_rec(self):
        return biffrecords.DateModeRecord(self.__dates_1904).get()

    def __precision_rec(self):
        return biffrecords.PrecisionRecord(self.__use_cell_values).get()

    def __refresh_all_rec(self):
        return biffrecords.RefreshAllRecord().get()

    def __bookbool_rec(self):
        return biffrecords.BookBoolRecord().get()

    def __all_fonts_num_formats_xf_styles_rec(self):
        return self.__styles.get_biff_data()

    def __palette_rec(self):
        return b''

    def __useselfs_rec(self):
        return biffrecords.UseSelfsRecord().get()

    def __boundsheets_rec(self, data_len_before, data_len_after, sheet_biff_lens):
        #  .................................
        # BOUNDSEHEET0
        # BOUNDSEHEET1
        # BOUNDSEHEET2
        # ..................................
        # WORKSHEET0
        # WORKSHEET1
        # WORKSHEET2
        boundsheets_len = 0
        for sheet in self.__worksheets:
            boundsheets_len += len(biffrecords.BoundSheetRecord(
                0x00, sheet.visibility, sheet.name, self.encoding
                ).get())

        start = data_len_before + boundsheets_len + data_len_after

        result = b''
        for sheet_biff_len,  sheet in zip(sheet_biff_lens, self.__worksheets):
            result += biffrecords.BoundSheetRecord(
                start, sheet.visibility, sheet.name, self.encoding
                ).get()
            start += sheet_biff_len
        return result

    def __all_links_rec(self):
        pieces = []

        def sorted_index(dictionary):
            return sorted(((index, key) for key, index in dictionary.items()))

        for idx, tag in sorted_index(self._supbook_xref):
            stype, snum = tag
            if stype == 'ownbook':
                rec = biffrecords.InternalReferenceSupBookRecord(len(self.__worksheets)).get()
                pieces.append(rec)
            elif stype == 'xcall':
                rec = biffrecords.XcallSupBookRecord().get()
                pieces.append(rec)
                for idx, name in sorted_index(self._xcall_xref):
                    rec = biffrecords.ExternnameRecord(
                        options=0,
                        index=0,
                        name=name,
                        fmla='\x02\x00\x1c\x17').get()
                    pieces.append(rec)
            else:
                raise Exception('unknown supbook stype %r' % stype)

        if len(self.__sheet_refs) > 0:
            # get references in index order
            temp = [ref for idx, ref in sorted_index(self.__sheet_refs)]
            externsheet_record = biffrecords.ExternSheetRecord(temp).get()
            pieces.append(externsheet_record)

        return b''.join(pieces)

    def __sst_rec(self):
        return self.__sst.get_biff_record()

    def __ext_sst_rec(self, abs_stream_pos):
        return b''
        #return biffrecords.ExtSSTRecord(abs_stream_pos, self.sst_record.str_placement,
        #self.sst_record.portions_len).get()

    def get_biff_data(self):
        before = b''.join([
            self.__bof_rec(),
            self.__intf_hdr_rec(),
            self.__intf_mms_rec(),
            self.__intf_end_rec(),
            self.__write_access_rec(),
            self.__codepage_rec(),
            self.__dsf_rec(),
            self.__tabid_rec(),
            self.__fngroupcount_rec(),
            self.__wnd_protect_rec(),
            self.__protect_rec(),
            self.__obj_protect_rec(),
            self.__password_rec(),
            self.__prot4rev_rec(),
            self.__prot4rev_pass_rec(),
            self.__backup_rec(),
            self.__hide_obj_rec(),
            self.__window1_rec(),
            self.__datemode_rec(),
            self.__precision_rec(),
            self.__refresh_all_rec(),
            self.__bookbool_rec(),
            self.__all_fonts_num_formats_xf_styles_rec(),
            self.__palette_rec(),
            self.__useselfs_rec(),
        ])

        country = self.__country_rec()
        all_links = self.__all_links_rec()

        shared_str_table = self.__sst_rec()
        after = country + all_links + shared_str_table

        ext_sst = self.__ext_sst_rec(0) # need fake cause we need calc stream pos
        eof = self.__eof_rec()

        self.__worksheets[self.__active_sheet].selected = True

        sheets = [sheet.get_biff_data() for sheet in self.__worksheets]
        sheet_biff_lens = map(len, sheets)

        bundlesheets = self.__boundsheets_rec(
            len(before),
            len(after)+len(ext_sst)+len(eof),
            sheet_biff_lens)

        sst_stream_pos = len(before) + len(bundlesheets) + len(country) \
                       + len(all_links)
        ext_sst = self.__ext_sst_rec(sst_stream_pos)

        return before + bundlesheets + after + ext_sst + eof + b''.join(sheets)

#Record Order in BIFF8
#  Workbook Globals Substream
#      BOF Type = workbook globals
#      Interface Header
#      MMS
#      Interface End
#      WRITEACCESS
#      CODEPAGE
#      DSF
#      TABID
#      FNGROUPCOUNT
#      Workbook Protection Block
#            WINDOWPROTECT
#            PROTECT
#            PASSWORD
#            PROT4REV
#            PROT4REVPASS
#      BACKUP
#      HIDEOBJ
#      WINDOW1
#      DATEMODE
#      PRECISION
#      REFRESHALL
#      BOOKBOOL
#      FONT +
#      FORMAT *
#      XF +
#      STYLE +
#    ? PALETTE
#      USESELFS
#
#      BOUNDSHEET +
#
#      COUNTRY
#    ? Link Table
#      SST
#      ExtSST
#      EOF
