#!/bin/sh

#BASE="http://localhost:17080/import_events"
BASE="http://hard-at-work.appspot.com/import_events"

ALL1="\
https://web.archive.org/web/20170317042819/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170318014748/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170319050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170320050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170321050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170322050006/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170323050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170324050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170325050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170326050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170327050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170328050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170329050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170330050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170331050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170401050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170402050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170403050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170404050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170405050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170406050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170407050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170408050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170409050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170410050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170411000957/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170412050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170413050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170414050001/https://www.whitehouse.gov/1600daily \
"

ALL2="\
https://web.archive.org/web/20170415050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170416050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170417050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170418003515/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170419050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170420050011/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170421050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170422050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170423050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170424050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170425050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170426050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170427050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170428050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170429050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170430050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170501050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170502050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170503050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170504050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170505050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170506050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170507050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170508050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170509050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170510050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170511050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170512050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170513043006/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170514050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170515050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170516050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170517005221/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170518050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170519050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170520050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170521050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170522050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170523050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170524050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170525050001/https://www.whitehouse.gov/1600daily \
"

ALL3="\
https://web.archive.org/web/20170526050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170527050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170528050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170529050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170530050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170531050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170601050007/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170602050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170603050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170604050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170605050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170606050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170607050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170608050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170609000735/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170610050006/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170611050003/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170612050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170613050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170614050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170615050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170616004819/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170617050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170618050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170619050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170620050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170621041234/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170622050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170623011327/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170624050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170625050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170626050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170627050002/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170628050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170629050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170630013724/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170701050001/https://www.whitehouse.gov/1600daily \
https://web.archive.org/web/20170702050002/https://www.whitehouse.gov/1600daily \
"

ALL=$ALL3

for url in $ALL; do
    req="$BASE?url=$url"
    echo $req
    open $req
done
