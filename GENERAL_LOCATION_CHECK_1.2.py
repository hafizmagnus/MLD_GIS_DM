# RlVDSyBZT1UgQlVERFkh

# ------------------------------------------------------------------------------
#  Name:        MLD Digitisation Attribute Check
#  Purpose:     Provide GIS Data Managers with a tool to check attributes
#
#  Author:      Muhammad Hafiz Bin Ishak Magnus
#
#  Created:     21/07/2016
#  Copyright:   (c) National Parks Board 2016
#  Licence:     Enterprise Perpetual
# ------------------------------------------------------------------------------

import base64
from collections import Counter
import os
import re

import arcpy

__version__ = '1.0'

# ------------------------------------------------------------------------------

# initialising parameters
error_count = 0
warning_count = 0
assigned_loc_cd_list = []
mod_loc_cd = []
all_loc_desc = []

# ---------------------

eu = 'TUxEX0dJU19WSUVX'
ep = 'TUxEZ2lzVmlld0AxMjM='

main_template = arcpy.GetParameterAsText(0)
folder = os.path.dirname(os.path.dirname(main_template))

con_path = folder + "\\" + "MAVEN_MLD_VIEW_TEMP.sde"

if os.path.exists(con_path):
    os.remove(con_path)

arcpy.CreateDatabaseConnection_management(folder, "MAVEN_MLD_VIEW_TEMP.sde", "SQL_SERVER", "NPMAVCLUS02\MSSQLSERVER1,60001", "DATABASE_AUTH", base64.decodestring(eu), base64.decodestring(ep), "SAVE_USERNAME", "Maven")

# ---------------------

# dictionary of the attributes and their aliases
attribute_alias = {
    "LOC_DESC": "Location Description", "SECTION_CODE": "Section Code",
    "AGENCY": "Agency", "EDIT_TYPE": "Edit Type"
}

# ---------------------

# dictionary of the accepted abbreviations
abbrv_dict = {
    'AYER RAJAH EXPRESSWAY': 'AYE', 'BUKIT TIMAH EXPRESSWAY': 'BKE', 'CENTRAL EXPRESSWAY': 'CTE',
    'EAST COAST PARKWAY': 'ECP', 'KRANJI EXPRESSWAY': 'KJE', 'KALLANG-PAYA LEBAR EXPRESSWAY': 'KPE',
    'KALLANG PAYA LEBAR EXPRESSWAY': 'KPE', 'SELETAR EXPRESSWAY': 'SLE',
    'PAN ISLAND EXPRESSWAY': 'PIE', 'TAMPINES EXPRESSWAY': 'TPE', 'MARINA COASTAL EXPRESSWAY': 'MCE',
    'ACCESS': 'ACCS', 'ALLEY': 'ALY', 'ALLEYWAY': 'ALWY', 'AMBLE': 'AMBL',
    'ANCHORAGE': 'ANCG', 'APPROACH': 'APP', 'ARCADE': 'ARC', 'ARTERY': 'ART',
    'AVENUE': 'AVE', 'BANK': 'BNK', 'BASIN': 'BASN', 'BAY': 'BY', 'BEACH': 'BH',
    'BEND': 'BND', 'BESIDE': 'B/S', 'BLOCK': 'BLK', 'BOULEVARD': 'BLVD',
    'BOUNDARY': 'BNDRY', 'BOWL': 'BWL', 'BRACE': 'BCE', 'BRANCH': 'BRCH', 'BREAK': 'BRK',
    'BRIDGE': 'BDGE', 'BROADWAY': 'BDWY', 'BROW': 'BR', 'BUILDING': 'BLD',
    'BUILDINGS': 'BLDS', 'BYPASS': 'BYPA', 'BYWAY': 'BYWY',
    'CAUSEWAY': 'CSWY', 'CENTRE': 'CNTR', 'CENTER': 'CNTR', 'CENTREWAY': 'CNTRWY', 'CHASE': 'CH', 'CIRCLE': 'CIR',
    'CIRCLET': 'CRCLT', 'CIRCUIT': 'CCT', 'CIRCUS': 'CRCS', 'CLOSE': 'CL',
    'COLONNADE': 'CLDE', 'COMMON': 'CMMN', 'COMMUNITY': 'COMM', 'CONCOURSE': 'CNCRSE',
    'CONNECTION': 'CNNCTN', 'COPSE': 'CPSE', 'CORNER': 'CNR', 'COURSE': 'CORS',
    'COURT': 'CRT', 'COURTYARD': 'CRTYD', 'CREEK': 'CK', 'CRESCENT': 'CRS',
    'CRIEF': 'CRF', 'CROSS': 'CRSS', 'CROSSING': 'CRSNG', 'CROSSROAD': 'CRD',
    'CROSSWAY': 'CRSWY', 'CRUISEWAY': 'CRUISWY', 'CUL DE SAC': 'CDS', 'CUTTING': 'CTTG',
    'DEVIATION': 'DVTN', 'DISTRIBUTOR': 'DSTR', 'DOWNS': 'DWNS', 'DRAIN RESERVE': 'D/R',
    'DRAINAGE RESERVE': 'D/R', 'DRIVE': 'DRV', 'DRIVEWAY': 'DRWY', 'EASEMENT': 'EASMNT',
    'EAST': 'E.', 'ELBOW': 'ELB', 'ENTRANCE': 'ENT', 'ESPLANADE': 'ESP', 'ESTATE': 'EST',
    'EXPRESSWAY': 'EXPWY', 'EXTENSION': 'EXT', 'FAIRWAY': 'FRWY', 'FIRE TRACK': 'FTRK',
    'FIRETRAIL': 'FITR', 'FOLLOW': 'FOLW', 'FOOTWAY': 'FTWY', 'FORESHORE': 'FSHR',
    'FORMATION': 'FORM', 'FORMER': 'FOMR.', 'FREEWAY': 'FWY', 'FRONT': 'FRNT', 'FRONTAGE': 'FRNTGE',
    'GARDEN': 'GARDN', 'GARDENS': 'GARDNS', 'GATE': 'GTE', 'GATES': 'GTES',
    'GATEWAY': 'GTWY', 'GRANGE': 'GRNGE', 'GREEN': 'GRN', 'GROUND': 'GRND',
    'GROVE': 'GR', 'GULLY': 'GLY', 'HEATH': 'HTH', 'HEIGHTS': 'HTS', 'HIGHROAD': 'HRD',
    'HIGHWAY': 'HWY', 'HILL': 'HL', 'HILLSIDE': 'HLSD', 'HOLLOW': 'HOLW', 'INTERCHANGE': 'INT',
    'INTERSECTION': 'INTN', 'ISLAND': 'IS', 'JUNCTION': 'JN', 'LANDING': 'LDG',
    'LANE': 'LN', 'LANEWAY': 'LNWY', 'LITTLE': 'LT', 'LOCATION': 'LCN', 'LOOKOUT': 'LKT',
    'LORONG': 'LOR', 'LOWER': 'LR', 'MEANDER': 'MNDR', 'MOTORWAY': 'MWY', 'MOUNT': 'MT',
    'NORTH': 'N.', 'OUTLOOK': 'OUTLK', 'PARADE': 'PDE', 'PARADISE': 'PDSE', 'PARK': 'PK',
    'PARKLANDS': 'PKLD', 'PARKWAY': 'PKWY', 'PATH': 'PTH', 'PATHWAY': 'PTHWY', 'PIAZZA': 'PIAZ',
    'PIER': 'PR', 'PLACE': 'PL', 'PLATEAU': 'PLAT', 'PLAZA': 'PLZ', 'PLOT': 'PLT', 'POCKET': 'PKT',
    'POINT': 'PT', 'PORT': 'PRT', 'PROMENADE': 'PRM', 'PURSUIT': 'PUR', 'QUADRANGLE': 'QDGL',
    'QUADRANT': 'QDT', 'QUAY': 'QY', 'QUAYS': 'QYS', 'RACECOURSE': 'RACECRSE', 'RAILWAY SIDING': 'RLYSDNG',
    'RANGE': 'RNGE', 'REACH': 'RCH', 'RESERVE': 'RSRVE', 'RESERVOIR': 'RES.', 'REST': 'RST', 'RETREAT': 'RET',
    'RETURN': 'RTRN', 'RIDE': 'RDE', 'RIDGE': 'RDG', 'RIDGEWAY': 'RGWY', 'RIGHT OF WAY': 'ROWY',
    'RIVER': 'RVR', 'RIVERWAY': 'RVWY', 'RIVIERA': 'RVRA', 'ROAD': 'RD', 'ROADS': 'RDS',
    'ROADSIDE': 'RDSIDE', 'ROADWAY': 'RDWY', 'RONDE': 'RNDE', 'ROSEBOWL': 'RSBL', 'ROTARY': 'RTY',
    'ROUND': 'RND', 'ROUTE': 'RTE', 'ROW': 'RW', 'ROWE': 'RWE', 'SCHOOL': 'SCH', 'SERVICE WAY': 'SWY',
    'SIDING': 'SDNG', 'SLOPE': 'SLPE', 'SOUND': 'SND', 'SOUTH': 'S.', 'SQUARE': 'SQ',
    'STAIRS': 'STRS', 'STATE HIGHWAY': 'SHWY', 'STATE LAND': 'S/L', 'STATELAND': 'S/L', 'STATION': 'STN',
    'STRAIGHT': 'STRGHT', 'STRAND': 'STRA', 'STREET': 'ST', 'STRIP': 'STP',
    'SUBWAY': 'SBWY', 'TARN': 'TN', 'TERRACE': 'TCE', 'THOROUGHFARE': 'TFARE', 'TOLLWAY': 'TLWY',
    'TOWER': 'TWR', 'TOWERS': 'TWRS', 'TRACE': 'TRCE', 'TRACK': 'TRK', 'TRAIL': 'TRL',
    'TRAILER': 'TRLR', 'TRIANGLE': 'TRI', 'TRUNKWAY': 'TKWY', 'UNDERPASS': 'UPAS', 'UPPER': 'UPP',
    'VALE': 'VL', 'VIADUCT': 'VDCT', 'VIEW': 'VW', 'VILLAS': 'VLLS', 'VISTA': 'VIS', 'WALK': 'WLK',
    'WALKWAY': 'WLKWY', 'WATERS': 'WTRS', 'WEST': 'W.', 'WHARF': 'WHF', 'WYND': 'WYD', 'YARD': 'YD',
    'ANG MO KIO': 'AMK', 'CHOA CHU KANG': 'CCK', 'LIM CHU KANG': 'LCK', 'TOA PAYOH': 'TPY'
}

# ---------------------

eve_mld = con_path + '\\' + r'Maven.OPS.EVE_GIS\Maven.OPS.EXTERNAL_AGENCY_LOCATION_BOUNDARY'
eve_pk = con_path + '\\' + r'Maven.OPS.EVE_GIS\Maven.OPS.PARK_MAINTENANCE_BOUNDARY'
eve_ss = con_path + '\\' + r'Maven.OPS.EVE_GIS\Maven.OPS.STREETSCAPE_LOCATION_BOUNDARY'

eve_layer_dict_a = {
    eve_mld: "other MLD Managed Areas",
    eve_pk: "Parks Managed Areas",
    eve_ss: "Streetsapce Managed Areas"
}

eve_layer_list_act = [eve_mld, eve_pk, eve_ss]

# list of row headings used
row_header = ["LOC_DESC", "SECTION_CODE", "AGENCY", "EDIT_TYPE"]



# ------------------------------------------------------------------------------


# function to check if the location code has been assigned internally
def internal_loc_cd_check(new_lc, assigned_loc_cd):
    global assigned_loc_cd_list
    if new_lc not in assigned_loc_cd:
        assigned_loc_cd.append(new_lc)
        return new_lc
    else:
        if new_lc.startswith("URA"):
            new_lc_prefix = new_lc[:3]
        else:
            new_lc_prefix = new_lc[:4]
        code_list = [int(x[-3:]) for x in assigned_loc_cd if x.startswith(new_lc_prefix)]
        code_list.sort(reverse=True)
        higher_number = code_list[0] + 1
        a_new_lc = new_lc_prefix + str(higher_number).zfill(3)
        assigned_loc_cd.append(a_new_lc)
        return a_new_lc


# function to abbreviate the location description if necessary
def abbreviator(s, d=abbrv_dict):
    pattern = re.compile(r'\b(' + '|'.join(d.keys()) + r')\b')
    return pattern.sub(lambda x: d[x.group()], s)

# ------------------------------------------------------------------------------


# this function checks that all mandatory fields are entered
# this also checks and populates location codes
def loc_attr_check(main_feature, eve_mld_loc=eve_mld, eve_layer_list=eve_layer_list_act, att_dict=attribute_alias,
                   headers=row_header, eve_layer_dict=eve_layer_dict_a, modified_loc_cd_list=mod_loc_cd, all_loc_desc_list=all_loc_desc):
    # main_feature -> MLD main location template
    # eve_mld_loc -> path to EXTERNAL AGENCY MANAGED AREA residing in MAVEN
    # eve_layer_list -> a python list of paths to the managed areas in MAVEN
    # att_dict -> dictionary of field names and their aliases
    # headers -> list of attributes in the cursors

    global error_count, warning_count, assigned_loc_cd_list, mod_loc_cd, all_loc_desc
    with arcpy.da.SearchCursor(main_feature, ["LOC_DESC", "SECTION_CODE", "AGENCY", "EDIT_TYPE", "LOC_CD", "OID@",
                                              "SHAPE@"]) as s_cursor:
        for a_row in s_cursor:
            arcpy.AddMessage("\nChecking the general attributes of Object ID {0}".format(a_row[5]))
            arcpy.GetMessages(0)
            all_loc_desc_list.append(a_row[0])

            # checking that all mandatory fields are filled
            for pos, attribute in enumerate(a_row[:4]):
                if not attribute:
                    arcpy.AddWarning(
                        "\tYou did not include a {0} for Object ID {1}".format(att_dict[(headers[pos])], a_row[5]))
                    arcpy.GetMessages(1)
                    error_count += 1
                    continue
                elif not str(attribute).strip():
                    arcpy.AddWarning(
                        "\tYou did not include a {0} for Object ID {1}".format(att_dict[(headers[pos])], a_row[5]))
                    arcpy.GetMessages(1)
                    error_count += 1
                    continue
                else:
                    arcpy.AddMessage("\t{0} OK!".format(att_dict[(headers[pos])]))
                    arcpy.GetMessages(0)

        if len(all_loc_desc_list) > 1:
            cnt = Counter(all_loc_desc_list)
            repeated_loc_desc = [x for x,v in cnt.iteritems() if v > 1]
            if len(repeated_loc_desc) > 0:
                for rep_loc_desc in repeated_loc_desc:
                    arcpy.AddWarning("\nThere are {0} polygons with the Location Description {1}".format(all_loc_desc_list.count(rep_loc_desc), rep_loc_desc))
                    arcpy.GetMessages(1)
                    warning_count += 1

        # re-setting the cursor to the start of the dataset to check the location codes
        s_cursor.reset()

        # ---------------------

        # checking the location code
        for b_row in s_cursor:
            counter = 0

            # location code for modifications must already exists for rows that pass the first round of checks
            if b_row[3] == 2 and (b_row[0] or str(b_row[0]).strip) and (b_row[1] or str(b_row[1]).strip) and (b_row[2] or str(b_row[2]).strip):
                arcpy.AddMessage("\nChecking the attributes for the modification of Object ID {0}.".format(b_row[5]))
                arcpy.GetMessages(0)
                if not (b_row[4] or str(b_row[4]).strip):
                    arcpy.AddWarning("\tYou did not include the Location Code for Object ID {0}.".format(b_row[5]))
                    arcpy.GetMessages(1)
                    error_count += 1
                    continue

                else:
                    lc_m_sql = """{0} = '{1}'""".format(arcpy.AddFieldDelimiters(eve_mld_loc, "LOC_CD"), b_row[4])
                    with arcpy.da.SearchCursor(eve_mld_loc, ["OID@", "LOC_CD", "LOC_DESC"],
                                               where_clause=lc_m_sql) as lc_cursor:
                        for mod in lc_cursor:
                            counter += 1
                            if mod[2] != b_row[0] and counter:
                                arcpy.AddWarning(
                                    "\tModification Warning: The Location Description for Object ID {0}, ({1}), does not match the corresponding Location Description in EVE ({2}).".format(
                                        b_row[5], b_row[0], mod[2]))
                                arcpy.GetMessages(1)
                                warning_count += 1
                            break
                        else:
                            arcpy.AddWarning(
                                "\tModification Error: For Object ID {0}, the location code {1} does not exists.".format(
                                    b_row[5], b_row[4]))
                            arcpy.GetMessages(1)
                            error_count += 1
                            continue

            # location codes for new managed areas must be an increase from the current location codes
            elif b_row[3] == 1 and (b_row[0] or str(b_row[0]).strip) and (b_row[1] or str(b_row[1]).strip) and (b_row[2] or str(b_row[2]).strip):
                arcpy.AddMessage("\nPopulating the Location Codes for Object ID {0}...".format(b_row[5]))
                arcpy.GetMessages(0)
                lc_n_sql = """{0} = {1}""".format(arcpy.AddFieldDelimiters(main_feature, "OBJECTID"), b_row[5])

                with arcpy.da.UpdateCursor(main_feature,
                                           ["LOC_DESC", "SECTION_CODE", "AGENCY", "EDIT_TYPE", "LOC_CD", "OID@",
                                            "SHAPE@"], where_clause=lc_n_sql) as lc_up_cursor:
                    for c_row in lc_up_cursor:

                        # getting the location codes for non-URA car parks
                        if c_row[2] != "URA":
                            biggest = 1  # initialising the location code number to 1
                            nu_number_list = []

                            try:
                                lc_prefix = str(c_row[1]) + str(c_row[2][0])

                            except TypeError:
                                arcpy.AddWarning("\tLocation Code not populated for Object ID {0}.".format(c_row[5]))
                                arcpy.GetMessages(1)
                                continue

                            sub_sql = """{0} LIKE '{1}%'""".format(arcpy.AddFieldDelimiters(eve_mld_loc, "LOC_CD"),
                                                                   lc_prefix)
                            with arcpy.da.SearchCursor(eve_mld_loc, ["LOC_CD"], where_clause=sub_sql) as eve_s_cursor:
                                # getting the new biggest running number if the prefix exists in MAVEN
                                for item in eve_s_cursor:
                                    nu_number_list = re.findall("[0-9]*", item[0])
                                    if len(nu_number_list) > 0:
                                        for x in nu_number_list:
                                            if x:
                                                running = int(x)
                                                if biggest < running:
                                                    biggest = running + 2
                            lc_no = biggest + 1
                            p_new_lc = lc_prefix + str(biggest).zfill(3)
                            c_row[4] = internal_loc_cd_check(p_new_lc, assigned_loc_cd_list)
                            lc_up_cursor.updateRow(c_row)
                            arcpy.AddMessage("\t{0} has been assigned the Location Code {1}".format(c_row[0], c_row[4]))
                            arcpy.GetMessages(0)

                        # getting the location codes for URA car parks
                        elif c_row[2] == 'URA':
                            biggest = 1  # initialising the count to 1
                            u_number_list = []

                            try:
                                lc_prefix = str(c_row[2])

                            except TypeError:
                                arcpy.AddWarning("\tLocation Code not populated for Object ID {0}.".format(c_row[5]))
                                arcpy.GetMessages(1)
                                continue

                            sub_sql_3 = """{0} LIKE '{1}%'""".format(arcpy.AddFieldDelimiters(eve_mld_loc, "LOC_CD"),
                                                                     lc_prefix)
                            with arcpy.da.SearchCursor(eve_mld_loc, ["LOC_CD"],
                                                       where_clause=sub_sql_3) as eve_s_cursor1:
                                # getting the new biggest running number from MAVEN
                                for item1 in eve_s_cursor1:
                                    u_number_list = re.findall("[0-9]*", item1[0])
                                    if len(u_number_list) > 0:
                                        for y in u_number_list:
                                            if y:
                                                urunning = int(y)
                                                if biggest < urunning:
                                                    biggest = urunning + 2

                            lc_no = biggest + 1
                            p_new_lc = lc_prefix + str(biggest).zfill(3)
                            c_row[4] = internal_loc_cd_check(p_new_lc, assigned_loc_cd_list)
                            lc_up_cursor.updateRow(c_row)
                            arcpy.AddMessage(
                                "\t{0} has been assigned the Location Code {1}".format(c_row[0], c_row[4]))
                            arcpy.GetMessages(0)

                            # re-setting the cursor to the start of the dataset to check the location description
        s_cursor.reset()

        # ---------------------

        # checking that the new location description conforms to MLD's naming convention
        for d_row in s_cursor:
            # only do this for lines that have the mandatory attributes
            if d_row[3] == 1 and (d_row[0] or d_row[0].strip())and (d_row[1] or d_row[1].strip())and (d_row[2] or d_row[2].strip()):
                arcpy.AddMessage("\nChecking the Location Description of Object ID {0}.".format(d_row[5]))
                arcpy.GetMessages(0)

                # correcting for user idiosyncracies
                i_desc = d_row[0].upper().replace('\\', '/').replace("  ", " ").strip()

                # for situations where the three char. agency suffix has been used
                if re.match("^[ABDHLMPRSU]{3}\s[-]\s", i_desc):
                    sql_statement = """{0} = {1}""".format(arcpy.AddFieldDelimiters(main_feature, "OBJECTID"),
                                                           d_row[5])
                    with arcpy.da.UpdateCursor(main_feature, ["LOC_DESC", "LOC_CD", "OID@"],
                                               where_clause=sql_statement) as ld_up_cursor:
                        for correcting_ld in ld_up_cursor:
                            pos = i_desc.index("-")
                            pos = pos + 1
                            p_desc = i_desc[pos:].strip()
                            f_desc = str(d_row[2]) + " - " + p_desc
                            correcting_ld[0] = f_desc
                            ld_up_cursor.updateRow(correcting_ld)
                            arcpy.AddMessage("\tLocation Description is OK!")
                            arcpy.GetMessages(0)

                # for situations where more two agencies prefix has been used e.g. SLA/HDB
                elif re.match("^[ABDHLMPRSU\/]{7}\s[-]\s", i_desc):
                    sql_statement = """{0} = {1}""".format(arcpy.AddFieldDelimiters(main_feature, "OBJECTID"),
                                                           d_row[5])
                    with arcpy.da.UpdateCursor(main_feature, ["LOC_DESC", "LOC_CD", "OID@"],
                                               where_clause=sql_statement) as ld_up_cursor:
                        for correcting_ld in ld_up_cursor:
                            f_desc = i_desc
                            correcting_ld[0] = f_desc
                            ld_up_cursor.updateRow(correcting_ld)
                            arcpy.AddMessage("\tLocation Description is OK!")
                            arcpy.GetMessages(0)

                # for situations where no agency prefix has been used
                else:
                    sql_statement = """{0} = {1}""".format(arcpy.AddFieldDelimiters(main_feature, "OBJECTID"),
                                                           d_row[5])
                    with arcpy.da.UpdateCursor(main_feature, ["LOC_DESC", "LOC_CD", "OID@"],
                                               where_clause=sql_statement) as ld_up_cursor:
                        for correcting_ld in ld_up_cursor:

                            if len(i_desc) <= 44:
                                f_desc = str(d_row[2]) + " - " + i_desc
                                arcpy.AddWarning(
                                    "\tThe location description {0} has been changed to {1}".format(i_desc, f_desc))
                                arcpy.GetMessages(1)
                                warning_count += 1
                                correcting_ld[0] = f_desc
                                ld_up_cursor.updateRow(correcting_ld)

                            else:
                                p_desc = abbreviator(i_desc)
                                if len(p_desc) > 44:
                                    p_desc = p_desc[:44]
                                f_desc = str(d_row[2]) + " - " + p_desc
                                arcpy.AddWarning(
                                    "\tThe location description {0} has been changed to {1}".format(i_desc, f_desc))
                                arcpy.GetMessages(1)
                                warning_count += 1
                                correcting_ld[0] = f_desc
                                ld_up_cursor.updateRow(correcting_ld)

        # re-setting the cursor to the start of the dataset to check the shape digitisation
        s_cursor.reset()

        # ---------------------

        # checking that the new locations does not overlap other Managed Areas
        for e_row in s_cursor:
            internal_counter = 0
            ly_c = 0

            # only do this for lines that have the mandatory attributes
            if e_row[3] == 1 and (e_row[0] or e_row[0].strip()) and (e_row[1] or e_row[1].strip()) and (e_row[2] or e_row[2].strip()):
                arcpy.AddMessage("\nChecking the new geometry of Object ID {0}.".format(e_row[5]))
                arcpy.GetMessages(0)

                geo_ok = 0

                # checking for live EVE managed areas
                for eve_layer in eve_layer_list:
                    ly_c += 1
                    clip_ly = "in_memory" + "\\" + "clip_layer" + str(ly_c)
                    arcpy.Clip_analysis(eve_layer, main_feature, clip_ly)
                    feature_count = arcpy.GetCount_management(clip_ly)
                    fc = int(feature_count.getOutput(0))
                    if fc > 0:
                        arcpy.AddWarning("\tThere are overlaps with {0}. Correcting overlaps...".format(
                            eve_layer_dict[eve_layer]))
                        arcpy.GetMessages(1)
                        with arcpy.da.UpdateCursor(main_feature, ["SHAPE@"]) as temp_polygon_geo:
                            for a_temp_geo in temp_polygon_geo:
                                with arcpy.da.SearchCursor(clip_ly, ["SHAPE@"]) as eve_polygon_geo:
                                    for an_eve_geo in eve_polygon_geo:
                                        try:
                                            a_temp_geo[0] = a_temp_geo[0].difference(an_eve_geo[0])
                                            temp_polygon_geo.updateRow(a_temp_geo)
                                        except:
                                            continue

                        arcpy.AddMessage("\tCorrections done!")
                        arcpy.GetMessages(0)

                    else:
                        geo_ok += 1
                        if geo_ok == 3:
                            arcpy.AddMessage("\tGeometry OK!")
                            arcpy.GetMessages(0)

                    arcpy.Delete_management(clip_ly)

                # checking for overlaps within the template itself
                internal_counter += 1
                self_sql = """{0} <> {1}""".format(arcpy.AddFieldDelimiters(main_feature, "OBJECTID"), e_row[5])
                itself_sql = """{0} = {1}""".format(arcpy.AddFieldDelimiters(main_feature, "OBJECTID"), e_row[5])
                internal_ly = "internal" + str(internal_counter)
                itself_ly = "itself" + str(internal_counter)
                internal_clip = "in_memory" + "\\" + "internal_clip_layer" + str(internal_counter)
                arcpy.MakeFeatureLayer_management(main_feature, internal_ly, where_clause=self_sql)
                arcpy.MakeFeatureLayer_management(main_feature, itself_ly, where_clause=itself_sql)
                arcpy.Clip_analysis(internal_ly, itself_ly, internal_clip)
                result_s_sbl = arcpy.GetCount_management(internal_clip)
                count_s_sbl = int(result_s_sbl.getOutput(0))

                # if there are possible overlaps, correct them
                if count_s_sbl > 0:
                    with arcpy.da.SearchCursor(internal_clip, ["SHAPE@", "OID@"]) as io_cursor:
                        for i_object in io_cursor:
                            try:
                                arcpy.AddWarning("\tThere are overlaps with Object ID {0}.Correcting overlaps...".format(i_object[1]))
                                arcpy.GetMessages(1)

                                i_up_sql_statement = """{0} = {1}""".format(
                                    arcpy.AddFieldDelimiters(main_feature, "OBJECTID"), e_row[5])
                                with arcpy.da.UpdateCursor(main_feature, ["SHAPE@", "OID@"],
                                                           where_clause=i_up_sql_statement) as i_shape_cursor:
                                    for i_up_shape in i_shape_cursor:
                                        i_up_shape[0] = e_row[6].difference(i_object[0])
                                        i_shape_cursor.updateRow(i_up_shape)

                                arcpy.AddMessage("\tCorrections done!")
                                arcpy.GetMessages(0)
                            except:
                                continue
                    arcpy.Delete_management(internal_ly)
                    arcpy.Delete_management(itself_ly)
                    arcpy.Delete_management(internal_clip)

                # if there are no possible overlaps, delete the temporary layer file
                else:
                    arcpy.Delete_management(internal_ly)
                    arcpy.Delete_management(itself_ly)
                    arcpy.Delete_management(internal_clip)

            # populating the modification list with the location codes of modified areas
            elif e_row[3] == 2 and (e_row[0] or str(e_row[0]).strip) and (e_row[1] or str(e_row[1]).strip) and (e_row[2] or str(e_row[2]).strip):
                if e_row[3] not in modified_loc_cd_list:
                    modified_loc_cd_list.append(e_row[3])

                # ---------------------

        # creating a new MLD layer specifically for the modification correction if there are any
        if len(modified_loc_cd_list) > 0:
            new_mld_mod_layer_sql = """NOT ({0} in {1})""".format(arcpy.AddFieldDelimiters(eve_mld_loc, "LOC_CD"),
                                                                  "('" + "', '".join(
                                                                      map(str, modified_loc_cd_list)) + "')")
            new_mld_layer = "NEW_MLD_LAYER_FOR_MODIFICATION"
            new_mld_layer_clip = "in_memory" + "\\" + "NEW_MLD_LAYER_CLIP"
            arcpy.MakeFeatureLayer_management(eve_mld_loc, new_mld_layer, where_clause=new_mld_mod_layer_sql)

            try:
                arcpy.Clip_analysis(new_mld_layer, main_feature, new_mld_layer_clip)

            except:
                arcpy.Delete_management(new_mld_layer_clip)
                arcpy.Clip_analysis(new_mld_layer, main_feature, new_mld_layer_clip)

            # re-setting the cursor to the start of the dataset to check the shape digitisation of modified areas
            s_cursor.reset()

            # checking that the shape digitisation of modified areas
            for f_row in s_cursor:

                # looking at each modified area in the list
                if f_row[3] == 2 and (f_row[0] or str(f_row[0]).strip) and (f_row[1] or str(f_row[1]).strip) and (f_row[2] or str(f_row[2]).strip):
                    arcpy.AddMessage("\nChecking the geometry modification of Object ID {0}.".format(f_row[5]))
                    arcpy.GetMessages(0)
                    with arcpy.da.SearchCursor(new_mld_layer_clip, ["SHAPE@", "OID@"]) as mod_geo_cursor:
                        for mod_polygon in mod_geo_cursor:
                            try:
                                if mod_polygon[0].within(f_row[6]) or mod_polygon[0].overlaps(f_row[6]) or mod_polygon[0].contains(f_row[6]) or mod_polygon[0].touches(f_row[6]):
                                    arcpy.AddWarning(
                                        "\tThere are overlaps with Object ID {0}.Correcting overlaps...".format(
                                            f_row[5]))
                                    arcpy.GetMessages(1)
                                    mod_corr_sql_statement = """{0} = {1}""".format(
                                        arcpy.AddFieldDelimiters(main_feature, "OBJECTID"), f_row[5])
                                    with arcpy.da.UpdateCursor(main_feature, ["SHAPE@", "OID@"],
                                                               where_clause=mod_corr_sql_statement) as mi_shape_cursor:
                                        for mi_shape in mi_shape_cursor:
                                            mi_shape[0] = f_row[6].difference(mod_polygon[0])
                                            mi_shape_cursor.updateRow(mi_shape)
                                            arcpy.AddMessage("\tCorrections done!")
                                            arcpy.GetMessages(0)
                                else:
                                    arcpy.AddMessage("\tGeometry OK!")
                                    arcpy.GetMessages(0)
                            except:
                                continue

                            # ---------------------

        # re-setting the cursor to the start of the dataset to check the shape digitisation of modified areas
        s_cursor.reset()
        m_internal_counter = 0

        for g_row in s_cursor:
            try:
                # checking for overlaps within the template itself for modification
                m_internal_counter += 1
                m_self_sql = """{0} <> {1}""".format(arcpy.AddFieldDelimiters(main_feature, "OBJECTID"), g_row[5])
                m_itself_sql = """{0} = {1}""".format(arcpy.AddFieldDelimiters(main_feature, "OBJECTID"), g_row[5])
                m_internal_ly = "m_internal" + str(m_internal_counter)
                m_itself_ly = "m_itself" + str(m_internal_counter)
                m_internal_clip = "in_memory" + "\\" + "m_internal_clip_layer" + str(m_internal_counter)
                arcpy.MakeFeatureLayer_management(main_feature, m_internal_ly, where_clause=m_self_sql)
                arcpy.MakeFeatureLayer_management(main_feature, m_itself_ly, where_clause=m_itself_sql)
                arcpy.Clip_analysis(m_internal_ly, m_itself_ly, m_internal_clip)
                m_result_s_sbl = arcpy.GetCount_management(m_internal_clip)
                m_count_s_sbl = int(m_result_s_sbl.getOutput(0))

                # if there are possible overlaps, correct them
                if m_count_s_sbl > 0:
                    with arcpy.da.SearchCursor(m_internal_clip, ["SHAPE@", "OID@"]) as mio_cursor:
                        for mi_object in mio_cursor:
                            try:
                                arcpy.AddWarning(
                                    "\tThere are overlaps with Object ID {0}.Correcting overlaps...".format(
                                        mi_object[1]))
                                arcpy.GetMessages(1)

                                mi_up_sql_statement = """{0} = {1}""".format(
                                    arcpy.AddFieldDelimiters(main_feature, "OBJECTID"), g_row[5])
                                with arcpy.da.UpdateCursor(main_feature, ["SHAPE@", "OID@"],
                                                           where_clause=mi_up_sql_statement) as mi_shape_cursor:
                                    for mi_up_shape in mi_shape_cursor:
                                        mi_up_shape[0] = g_row[6].difference(mi_object[0])
                                        mi_shape_cursor.updateRow(mi_up_shape)

                                arcpy.AddMessage("\tCorrections done!")
                                arcpy.GetMessages(0)

                                arcpy.Delete_management(m_internal_ly)
                                arcpy.Delete_management(m_itself_ly)
                                arcpy.Delete_management(m_internal_clip)

                            except:
                                continue

                else:
                    arcpy.Delete_management(m_internal_ly)
                    arcpy.Delete_management(m_itself_ly)
                    arcpy.Delete_management(m_internal_clip)
            except:
                continue

        arcpy.AddMessage("\nGeometry checks completed!")
        arcpy.GetMessages(0)

    # ---------------------

    # removing null geometry
    arcpy.RepairGeometry_management(main_feature)


# ------------------------------------------------------------------------------

loc_attr_check(main_template)

os.remove(con_path)

if error_count or warning_count:
    arcpy.AddMessage("\nThe tool completed with {0} errors and {1} warnings\n".format(error_count, warning_count))
    arcpy.GetMessages(0)
