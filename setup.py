
import setuptools

setuptools.setup(
    name="scgv",
    version="1.1.0",
    author="Lubomir Chorbadjiev",
    author_email="lubomir.chorbadjiev@gmail.com",
    description="SCGV is an interactive graphical tool for single-cell "
    "genomics data, with emphasis on single-cell genomics of cancer",
    long_description="""SCGV is an interactive graphical tool for 
        single-cell genomics data, with
        emphasis on single-cell genomics of cancer. It facilitates examination, jointly
        or individually, of DNA copy number profiles of cells harvested from
        multiple anatomic locations (sectors). In the opening view the copy-number
        data matrix, with columns corresponding to cells and rows to genomic locations,
        is represented as a heat map with color-encoded integer DNA copy number. If a
        phylogenetic tree is available for the cells comprising the dataset, it can be
        used to order the columns of the data matrix, and clones formed by closely
        related cells may be identified. Alternatively, the columns
        can be ordered by the sector of origin of the cells. Cyto-pathological
        information may be displayed in a separate view, including sector-specific
        slide images and pathology reports. Genomic sub-regions and
        random subsets of cells can be selected and zoomed into. Individual or multiple
        copy-number profiles may be plotted as copy number against the genomic
        coordinate, and these plots may again be zoomed into. Chromosomal regions
        selected within the profiles may be followed to UCSC genome browser to
        examine the genomic context.""",
    url="https://github.com/KrasnitzLab/SCGV",
    packages=setuptools.find_packages(
        # 'scgv',
        exclude=['docs', 'tests']
    ),
    package_data={
        'scgv.qtviews': ['icons/*.png'],
    },
    include_package_data=True,
    # package_dir={'':'scgv'},
    entry_points={
        'console_scripts': [
            'scgview=scgv.qtmain:main',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    
)
