# $ pipenv run python ./run.py
from daemon import call_aprocess


lmafilelist = """
Z:\\2019A8045Fukuzawa\\lma_files\\aq000__0000.lma
Z:\\2019A8045Fukuzawa\\lma_files\\aq000__0001.lma
Z:\\2019A8045Fukuzawa\\lma_files\\aq000__0002.lma
""".split()
workingdir = "D:\\2019A8045Fukuzawa\\hit_files\\aq000_0000--0002"

call_aprocess(
    lmafilelist=lmafilelist,
    workingdir=workingdir,
)
