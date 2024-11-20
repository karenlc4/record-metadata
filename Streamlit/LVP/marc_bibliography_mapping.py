marc_field_mapping_bibliographic = {

    # Leader and Control Fields
    '000': '000-Leader',
    '001': '001-Control Number',
    '003': '003-Control Number Identifier',
    '005': '005-Date and Time of Latest Transaction',
    '006': '006-Fixed-Length Data Elements-Additional Material Characteristics',
    '007': '007-Physical Description Fixed Field-General Information',
    '008': '008-Fixed-Length Data Elements-General Information',

    # ISBN and ISSN
    '020': {
        'a': '020$a-International Standard Book Number (ISBN)',
        'c': '020$c-Terms of availability',
        'q': '020$q-Qualifying information',
        'z': '020$z-Canceled/invalid ISBN'
    },
    '022': {
        'a': '022$a-International Standard Serial Number (ISSN)',
        'y': '022$y-Incorrect ISSN',
        'z': '022$z-Canceled/invalid ISSN'
    },

    # Control Numbers and Cataloging Source
    '035': {
        'a': '035$a-System control number',
        'z': '035$z-Canceled/invalid control number'
    },
    '040': {
        'a': '040$a-Cataloging source',
        'b': '040$b-Language of cataloging',
        'c': '040$c-Transcribing agency',
        'd': '040$d-Modifying agency',
        'e': '040$e-Description conventions'
    },
    '041': {
        'a': '041$a-Language code of text',
        'b': '041$b-Language code of summary',
        'd': '041$d-Language code of spoken text',
        'h': '041$h-Language code of original work'
    },

    # Classification Numbers
    '082': {
        'a': '082$a-Dewey Decimal Classification number',
        '2': '082$2-Edition number'
    },

    # Main Entry Fields (Personal, Corporate)
    '100': {
        'a': '100$a-Personal name',
        'b': '100$b-Numeration',
        'c': '100$c-Titles and other words associated with a name',
        'd': '100$d-Dates associated with a name',
        'q': '100$q-Fuller form of name'
    },
    '110': {
        'a': '110$a-Corporate name',
        'b': '110$b-Subordinate unit',
        'n': '110$n-Number of meeting',
        'd': '110$d-Date of meeting'
    },

    # Titles
    '245': {
        'a': '245$a-Title',
        'b': '245$b-Remainder of title',
        'c': '245$c-Statement of responsibility',
        'f': '245$f-Inclusive dates',
        'g': '245$g-Bulk dates',
        'h': '245$h-Medium',
        'k': '245$k-Form',
        'i': '245$i-Relationship information',
        'p': '245$p-Name of part/section of work'
    },

    # Edition, Imprint, and Dates
    '250': {
        'a': '250$a-Edition statement',
        'b': '250$b-Remainder of edition statement'
    },
    '260': {
        'a': '260$a-Place of publication, distribution, etc.',
        'b': '260$b-Name of publisher, distributor, etc.',
        'c': '260$c-Date of publication'
    },
    '264': {
        'a': '264$a-Place of production, publication, distribution, manufacture',
        'b': '264$b-Name of producer, publisher, distributor, manufacturer',
        'c': '264$c-Date of production, publication, or distribution'
    },

    # Physical Description
    '300': {
        'a': '300$a-Extent',
        'b': '300$b-Other physical details',
        'c': '300$c-Dimensions',
        'e': '300$e-Accompanying material'
    },

    # Series
    '490': {
        'a': '490$a-Series statement',
        'v': '490$v-Volume number',
        'l': '490$l-Language of the series'
    },
    '830': {
        'a': '830$a-Series added entry',
        'v': '830$v-Volume number'
    },

    # Subject Access Fields
    '600': {
        'a': '600$a-Personal name',
        'd': '600$d-Dates associated with a name',
        'v': '600$v-Form subdivision',
        'x': '600$x-General subdivision',
        'z': '600$z-Geographic subdivision',
        'j': '600$j-Relator term',
        'e': '600$e-Relator code'
    },
    '610': {
        'a': '610$a-Corporate name',
        'b': '610$b-Subordinate unit',
        'd': '610$d-Dates associated',
        'v': '610$v-Form subdivision',
        'x': '610$x-General subdivision',
        'z': '610$z-Geographic subdivision'
    },
    '650': {
        'a': '650$a-Topical term',
        'v': '650$v-Form subdivision',
        'x': '650$x-General subdivision',
        'y': '650$y-Chronological subdivision',
        'z': '650$z-Geographic subdivision'
    },

    # Notes
    '500': {
        'a': '500$a-General note'
    },
    '501': {
        'a': '501$a-With note'
    },
    '504': {
        'a': '504$a-Bibliography note'
    },
    '505': {
        'a': '505$a-Formatted contents note'
    },
    '520': {
        'a': '520$a-Summary note'
    },

    # Language and Publication Details
    '546': {
        'a': '546$a-Language note'
    },

    # Electronic Access and Linking Fields
    '856': {
        'u': '856$u-Uniform Resource Identifier (URI)',
        'z': '856$z-Public note',
        'y': '856$y-Link text',
        '7': '856$7-Access status'
    },

    # Other Standard Numbers
    '024': {
        'a': '024$a-Other Standard Identifier',
        'c': '024$c-Qualifier',
        'z': '024$z-Canceled/invalid identifier'
    },

    # Music and Related Fields
    '028': {
        'a': '028$a-Publisher or Distributor Number',
        'b': '028$b-Issuing body',
        'c': '028$c-Source',
        'q': '028$q-Qualifier'
    },

    # Dates Associated with Entities
    '046': {
        'a': '046$a-Special coded dates',
        'b': '046$b-Date resource modified',
        'j': '046$j-Date of last transaction'
    },

    # Linking Entries and Other Titles
    '775': {
        'a': '775$a-Other edition entry',
        't': '775$t-Title',
        'z': '775$z-ISSN or ISBN'
    },

    # Additional Linking Fields
    '880': {
        'a': '880$a-Alternate graphic representation'
    },

    # Personal Names - Relator Terms
    '700': {
        'a': '700$a-Personal name',
        'b': '700$b-Numeration',
        'c': '700$c-Titles and words associated with name',
        'd': '700$d-Dates associated with name',
        'e': '700$e-Relator term',
        't': '700$t-Title of a work'
    },

    # Added Entry Fields
    '710': {
        'a': '710$a-Corporate name',
        'b': '710$b-Subordinate unit',
        'e': '710$e-Relator term'
    },
    '730': {
        'a': '730$a-Uniform title'
    },

    # Uniform Titles
    '240': {
        'a': '240$a-Uniform title',
        'd': '240$d-Date of work',
        'f': '240$f-Date of performance',
        'g': '240$g-Medium of performance',
        'h': '240$h-Other distinguishing characteristics',
        'm': '240$m-Arranged statement',
        'n': '240$n-Number of part/section'
    },

    # Former Titles
    '247': {
        'a': '247$a-Former title',
        'b': '247$b-Remainder of former title'
    },

    # Standard Identifier Fields
    '010': {
        'a': '010$a-Library of Congress Control Number (LCCN)',
        'z': '010$z-Canceled/invalid LCCN'
    },
    '013': {
        'a': '013$a-Patent Control Number',
        'b': '013$b-Country Code',
        'c': '013$c-Kind of Patent'
    },

    # Rights and Permissions
    '540': {
        'a': '540$a-Terms Governing Use and Reproduction',
        'b': '540$b-Jurisdiction',
        'c': '540$c-Authorized users'
    },

    # Additional Descriptive Fields
    '245': {
        'i': '245$i-Relationship information',
        'p': '245$p-Name of part/section of work'
    },

    # Dates of Publication and Associated Events
    '362': {
        'a': '362$a-Dates of publication and/or sequential designation',
        'b': '362$b-Source of information'
    },

    # Data from Archival Holdings
    '351': {
        'a': '351$a-Organization and arrangement of materials',
        'b': '351$b-Hierarchical level'
    },

    # Rights and Reproduction
    '542': {
        'a': '542$a-Information about copyright status',
        'b': '542$b-Copyright owner',
        'f': '542$f-Copyright term'
    },

    # Holdings and Locations
    '852': {
        'a': '852$a-Location (institution)',
        'b': '852$b-Sublocation or collection',
        'c': '852$c-Shelving location',
        'h': '852$h-Classification part',
        'i': '852$i-Item part'
    },

    # Materials and Formats
    '340': {
        'a': '340$a-Physical medium',
        'b': '340$b-Dimensions',
        'c': '340$c-Material base and configuration'
    },

    # Provenance Fields
    '561': {
        'a': '561$a-Provenance',
        'b': '561$b-Immediate source of acquisition'
    },

    # Linked Resources (Multiple Formats)
    '773': {
        'a': '773$a-Host item entry',
        't': '773$t-Title',
        'g': '773$g-Related parts'
    },

    # Series Statements
    '490': {
        'a': '490$a-Series statement',
        'v': '490$v-Volume number',
        'l': '490$l-Language of the series'
    },

    # Author-Title Main Entry
    '700': {
        't': '700$t-Title of a work'
    }
}


marc_field_mapping_bibliographic_flat = {
    # Leader and Control Fields
    '000': '000-Leader',
    '001': '001-Control Number',
    '003': '003-Control Number Identifier',
    '005': '005-Date and Time of Latest Transaction',
    '006': '006-Fixed-Length Data Elements-Additional Material Characteristics',
    '007': '007-Physical Description Fixed Field-General Information',
    '008': '008-Fixed-Length Data Elements-General Information',

    # ISBN and ISSN
    '020$a': '020$a-International Standard Book Number (ISBN)',
    '020$c': '020$c-Terms of availability',
    '020$q': '020$q-Qualifying information',
    '020$z': '020$z-Canceled/invalid ISBN',

    '022$a': '022$a-International Standard Serial Number (ISSN)',
    '022$y': '022$y-Incorrect ISSN',
    '022$z': '022$z-Canceled/invalid ISSN',

    # Control Numbers and Cataloging Source
    '035$a': '035$a-System control number',
    '035$z': '035$z-Canceled/invalid control number',

    '040$a': '040$a-Cataloging source',
    '040$b': '040$b-Language of cataloging',
    '040$c': '040$c-Transcribing agency',
    '040$d': '040$d-Modifying agency',
    '040$e': '040$e-Description conventions',

    '041$a': '041$a-Language code of text',
    '041$b': '041$b-Language code of summary',
    '041$d': '041$d-Language code of spoken text',
    '041$h': '041$h-Language code of original work',

    # Classification Numbers
    '082$a': '082$a-Dewey Decimal Classification number',
    '082$2': '082$2-Edition number',

    # Main Entry Fields (Personal, Corporate)
    '100$a': '100$a-Personal name',
    '100$b': '100$b-Numeration',
    '100$c': '100$c-Titles and other words associated with a name',
    '100$d': '100$d-Dates associated with a name',
    '100$q': '100$q-Fuller form of name',

    '110$a': '110$a-Corporate name',
    '110$b': '110$b-Subordinate unit',
    '110$n': '110$n-Number of meeting',
    '110$d': '110$d-Date of meeting',

    # Titles
    '245$a': '245$a-Title',
    '245$b': '245$b-Remainder of title',
    '245$c': '245$c-Statement of responsibility',
    '245$f': '245$f-Inclusive dates',
    '245$g': '245$g-Bulk dates',
    '245$h': '245$h-Medium',
    '245$k': '245$k-Form',
    '245$i': '245$i-Relationship information',
    '245$p': '245$p-Name of part/section of work',

    # Edition, Imprint, and Dates
    '250$a': '250$a-Edition statement',
    '250$b': '250$b-Remainder of edition statement',

    '260$a': '260$a-Place of publication, distribution, etc.',
    '260$b': '260$b-Name of publisher, distributor, etc.',
    '260$c': '260$c-Date of publication',

    '264$a': '264$a-Place of production, publication, distribution, manufacture',
    '264$b': '264$b-Name of producer, publisher, distributor, manufacturer',
    '264$c': '264$c-Date of production, publication, or distribution',

    # Physical Description
    '300$a': '300$a-Extent',
    '300$b': '300$b-Other physical details',
    '300$c': '300$c-Dimensions',
    '300$e': '300$e-Accompanying material',

    # Series
    '490$a': '490$a-Series statement',
    '490$v': '490$v-Volume number',
    '490$l': '490$l-Language of the series',

    '830$a': '830$a-Series added entry',
    '830$v': '830$v-Volume number',

    # Subject Access Fields
    '600$a': '600$a-Personal name',
    '600$d': '600$d-Dates associated with a name',
    '600$v': '600$v-Form subdivision',
    '600$x': '600$x-General subdivision',
    '600$z': '600$z-Geographic subdivision',
    '600$j': '600$j-Relator term',
    '600$e': '600$e-Relator code',

    '610$a': '610$a-Corporate name',
    '610$b': '610$b-Subordinate unit',
    '610$d': '610$d-Dates associated',
    '610$v': '610$v-Form subdivision',
    '610$x': '610$x-General subdivision',
    '610$z': '610$z-Geographic subdivision',

    '650$a': '650$a-Topical term',
    '650$v': '650$v-Form subdivision',
    '650$x': '650$x-General subdivision',
    '650$y': '650$y-Chronological subdivision',
    '650$z': '650$z-Geographic subdivision',

    # Notes
    '500$a': '500$a-General note',
    '501$a': '501$a-With note',
    '504$a': '504$a-Bibliography note',
    '505$a': '505$a-Formatted contents note',
    '520$a': '520$a-Summary note',

    # Language and Publication Details
    '546$a': '546$a-Language note',

    # Electronic Access and Linking Fields
    '856$u': '856$u-Uniform Resource Identifier (URI)',
    '856$z': '856$z-Public note',
    '856$y': '856$y-Link text',
    '856$7': '856$7-Access status',

    # Other Standard Numbers
    '024$a': '024$a-Other Standard Identifier',
    '024$c': '024$c-Qualifier',
    '024$z': '024$z-Canceled/invalid identifier',

    # Music and Related Fields
    '028$a': '028$a-Publisher or Distributor Number',
    '028$b': '028$b-Issuing body',
    '028$c': '028$c-Source',
    '028$q': '028$q-Qualifier',

    # Dates Associated with Entities
    '046$a': '046$a-Special coded dates',
    '046$b': '046$b-Date resource modified',
    '046$j': '046$j-Date of last transaction',

    # Linking Entries and Other Titles
    '775$a': '775$a-Other edition entry',
    '775$t': '775$t-Title',
    '775$z': '775$z-ISSN or ISBN',

    # Additional Linking Fields
    '880$a': '880$a-Alternate graphic representation',

    # Personal Names - Relator Terms
    '700$a': '700$a-Personal name',
    '700$b': '700$b-Numeration',
    '700$c': '700$c-Titles and words associated with name',
    '700$d': '700$d-Dates associated with name',
    '700$e': '700$e-Relator term',
    '700$t': '700$t-Title of a work',

    # Added Entry Fields
    '710$a': '710$a-Corporate name',
    '710$b': '710$b-Subordinate unit',
    '710$e': '710$e-Relator term',

    '730$a': '730$a-Uniform title',

    # Uniform Titles
    '240$a': '240$a-Uniform title',
    '240$d': '240$d-Date of work',
    '240$f': '240$f-Date of performance',
    '240$g': '240$g-Medium of performance',
    '240$h': '240$h-Other distinguishing characteristics',
    '240$m': '240$m-Arranged statement',
    '240$n': '240$n-Number of part/section',

    # Former Titles
    '247$a': '247$a-Former title',
    '247$b': '247$b-Remainder of former title',

    # Standard Identifier Fields
    '010$a': '010$a-Library of Congress Control Number (LCCN)',
    '010$z': '010$z-Canceled/invalid LCCN',

    '013$a': '013$a-Patent Control Number',
    '013$b': '013$b-Country Code',
    '013$c': '013$c-Kind of Patent',

    # Rights and Permissions
    '540$a': '540$a-Terms Governing Use and Reproduction',
    '540$b': '540$b-Jurisdiction',
    '540$c': '540$c-Authorized users',

    # Additional Descriptive Fields
    '245$i': '245$i-Relationship information',
    '245$p': '245$p-Name of part/section of work',

    # Dates of Publication and Associated Events
    '362$a': '362$a-Start date of publication',
    '362$b': '362$b-End date of publication',

    # Holdings Information
    '856$3': '856$3-Display text',
}

