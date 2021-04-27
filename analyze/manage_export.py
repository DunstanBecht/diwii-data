#!/usr/bin/env python
# coding: utf-8

"""Source: dunstan.becht.network"""

    #========= IMPORTS ===================================================#

import tools.terminals
import tools.selections
import codes.survey

    #========= TERMINAL ==================================================#

print("Tool for exporting figures, maps or spreadsheets.")
tools.terminals.stopInfo()

if tools.terminals.do("export data 'insee'"):
    import export.insee

    if tools.terminals.do("export maps"):
        export.insee.map(tools.selections.MAIN["D"])
        export.insee.map(tools.selections.MAIN["E"])
        if tools.terminals.do("export for all divisions"):
            for division in tools.selections.DIVISIONS:
                selection = tools.selections.DIVISIONS[division]
                export.insee.map(selection)

    if tools.terminals.do("export figures 'establishments by workforce'"):
        export.insee.figureEstablishmentsByWorkforce(tools.selections.MAIN["D"],
                                                     tools.selections.MAIN["E"])
        if tools.terminals.do("export for all divisions"):
            for division in tools.selections.DIVISIONS:
                selection = tools.selections.DIVISIONS[division]
                export.insee.figureEstablishmentsByWorkforce(selection)

    if tools.terminals.do("export figures 'establishments by division'"):
        export.insee.figureEstablishmentsByDivision(tools.selections.MAIN["D"],
                                                    tools.selections.MAIN["E"])

    if tools.terminals.do("export figures 'enterprises by division'"):
        export.insee.figureEnterprisesByDivision(tools.selections.MAIN["D"],
                                                 tools.selections.MAIN["E"])

    if tools.terminals.do("export figures 'enterprises by owned establishments'"):
        export.insee.figureEnterprisesByOwnedEstablishments(tools.selections.MAIN["D"],
                                                            tools.selections.MAIN["E"])
        if tools.terminals.do("export for all divisions"):
            for division in tools.selections.DIVISIONS:
                selection = tools.selections.DIVISIONS[division]
                export.insee.figureEnterprisesByOwnedEstablishments(selection)

if tools.terminals.do("export data 'survey'"):
    import export.survey

    if tools.terminals.do("export figures 'representativeness'"):
        export.survey.figureEstablishmentsByDivision(tools.selections.MAIN["C"],
                                                  tools.selections.MAIN["R"])
        export.survey.figureEstablishmentsByWorkforce(tools.selections.MAIN["C"],
                                                      tools.selections.MAIN["R"])

    if tools.terminals.do("export spreadsheet 'results'"):
        export.survey.spreadsheetResults()

    partitions = [
        [
            [
                tools.selections.MAIN["MX"],
                tools.selections.MAIN["MY"],
                tools.selections.MAIN["PX"],
                tools.selections.MAIN["PY"],
            ],
            tools.selections.MAIN["R"],
        ],
        [
            [
                tools.selections.MAIN["X"],
                tools.selections.MAIN["Y"],
            ],
            tools.selections.MAIN["R"],
        ],
        [
            [
                tools.selections.groupByEnterprise(tools.selections.MAIN["M"]),
                tools.selections.groupByEnterprise(tools.selections.MAIN["P"]),
            ],
            tools.selections.groupByEnterprise(tools.selections.MAIN["R"]),
        ]

    ]

    if tools.terminals.do("check partitions"):
        for p in partitions:
            tools.selections.checkPartition(p[0], p[1])

    if tools.terminals.do("export figures 'answers'"):
        for selections, union in partitions:
            export.survey.figurePourcentages(1, selections)
            export.survey.figurePourcentages(2, selections)
            export.survey.figurePourcentages(3, selections)
            export.survey.figurePourcentages(4, selections)
            data5 = []
            for s in selections:
                data5.append([
                    export.survey.pourcentage("answer5", s, 'a'),
                    export.survey.pourcentage("answer5", s, 'b'),
                    export.survey.pourcentage("answer5", s, 'c'),
                    export.survey.pourcentage("answer5", s, 'd'),
                    export.survey.pourcentage("answer5", s, 'e'),
                ])
            export.survey.figurePourcentages(5, selections, data5, False)
            export.survey.figurePourcentages(6, selections, None, False)

    if tools.terminals.do("export text 'answers'"):
        export.survey.listTextAnswer(*[tools.selections.groupByEnterprise(p) for p in partitions[0][0]])

if tools.terminals.do("export data 'aif'"):
    import export.aif

    export.aif.figureTopics(tools.selections.MAIN["W"],
                            tools.selections.MAIN["Y"])
    export.aif.figureLevers(tools.selections.MAIN["W"],
                            tools.selections.MAIN["Y"])

if tools.terminals.do("export data 'contacts'"):
    import export.contacts

    export.contacts.spreadsheet()

if tools.terminals.do("export data 'report'"):
    import export.report

    if tools.terminals.do("export 'selections.tex'"):
        export.report.selections()

    if tools.terminals.do("export 'i2df.tex'"):
        export.report.i2df()

tools.terminals.finished()
