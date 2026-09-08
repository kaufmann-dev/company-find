Neither modeled company offers a demonstrated discount at the researched prices. CF Industries is a strong cost-positioned nitrogen producer, but its $134.99 price compares with a probability-weighted present value of $68.20. Global Ship Lease has valuable contracted charter income, but its $45.21 price compares with $26.41 after fleet replacement commitments and eventual vessel depletion. These are rejected comparison cases, not short recommendations. Mosaic and ICL remain unconfirmed research candidates; neither passes from narrative to a defensible recommendation here.

Research date: September 8, 2026, UTC. Final CF observation: 15:02 UTC minute bar, $134.99; GSL observation: 15:00 UTC minute bar, $45.21. These delayed intraday observations were captured at 15:18:28 UTC; they are not executable live prices or daily closes. Final raw data are in [quote_capture.json](../../outputs/quote_capture.json); the earlier exploratory snapshot remains preserved in sources.json. Share counts and balance-sheet inputs are synchronized through disclosed corporate events, but the actual September cash balances and all intervening repurchases are unavailable. The investment horizon ends September 8, 2031; company-specific annual operating forecasts extend through 2035, followed by an explicit CF reinvestment transition through 2040. GSL retains its finite 2035 fleet residual. Available tools were Massive snapshots, ticker reference, split/dividend records, web search/open of primary disclosures, and the local Python valuation engine. Massive financial-statement endpoints returned NOT_ENTITLED; planned primary filings supplied those statements. Direct consensus and absolute global segment-capacity feeds were unavailable. Raw market responses and source metadata are preserved in sources.json. No non-US local price is invented.

The discovery sequence started with food production and trade movement. Farmers pay from crop proceeds and seasonal credit for yield; nitrogen, potash, phosphate, sulfur, logistics, and retail application sit upstream. Cheap gas can benefit a nitrogen producer, whereas scarce sulfur can hurt a phosphate producer despite high fertilizer prices. Cargo owners pay ocean freight from traded-goods economics; liners purchase ship time, fuel, terminal services, and inland transport. A longer route can increase ship demand without increasing goods purchased, and route restoration can release capacity without any fall in trade. LNG transport was screened separately because liquefaction additions create cargoes while the simultaneous ship orderbook can absorb the benefit. Eleven investigated companies span nitrogen, potash/phosphate and farm retail, specialty minerals, container leasing, liner logistics, product/crude tankers, LNG shipping, and liquefaction. The complete role/mechanism/source/decision record is screened.json; sources are distinct only where the underlying evidence is distinct.

CF's causal chain is: sustained crop nutrient replacement [observed requirement] → fertilizer spending constrained by crop margins [inferred] → some recovery of stranded global supply and new capacity by 2028-30 [industry forecast plus own timing] → CF sold volumes recover after repairs, while product prices normalize [own forecast] → North American gas advantage preserves positive cash margins [observed mechanism; assumed future magnitude] → Blue Point consumes construction cash before contributing [disclosed commitments plus assumed ramp] → cash attributable to CF common shareholders after CHS and partner claims [calculated]. Neither rising global food consumption nor low-carbon importance establishes cheapness.

FAO's September 4 cereal brief puts 2026/27 utilization at 2,965 million tonnes and stocks/use at 31.6%, a weak basis for assuming extraordinary crop demand. IFA's May 19 outlook estimates fertilizer nitrogen use of 118.9 Mt in 2025/26 and approximately 123.6 Mt in 2030/31, against 17 Mt of additional nitrogen production capability over 2026-30. These are a trade association's forecasts, not certain outcomes. Its capability already incorporates achievable utilization; multiplying it again by a generic utilization/yield assumption would understate supply. Industrial nitrogen uses must also be separated before comparing capability with agricultural demand. [FAO, September 4, 2026, production/utilization/stocks](https://www.fao.org/worldfoodsituation/csdb); [IFA, May 19, 2026, pp.11-12 and 19-26](https://www.fertilizer.org/wp-content/uploads/2026/05/2026_IFA_Medium_Term_Outlook_Report_English.pdf).

My demand model uses cereal utilization as a transparent proxy for a proportionate wider crop basket, calibrated to fertilizer nitrogen consumption; it does not claim that all nitrogen is applied to cereals. Base crop activity grows 1.3% annually, nutrient use per activity declines 0.3%, and temporary affordability discounts reduce financially supported purchases in 2027-28. The resulting base fertilizer requirement grows about 1% annually after recovery. Efficiency saves nitrogen per unit but does not erase the crop growth; it also does not create an assumed rebound large enough to sustain shortage prices. Desired, affordable, available, and fulfilled demand are separate columns in inputs.json. Global inventory changes and precise industrial-use data are unresolved, so calculated headroom is potential supply, not asserted inventory accumulation.

The supply paths use an explicitly assumed 174 Mt starting productive nitrogen capability, anchored to IFA's 166.6 Mt observation for 2024 and its subsequent expansion forecasts. Industrial use starts at an assumed 40 Mt, with a 35-45 Mt sensitivity range. Base supply additions outpace crop requirement growth before economic closures respond. Scarcity remains regional because feedstock, sanctions, transport, product mix, and cash affordability prevent global capability from being fully interchangeable. The persistent-scarcity path combines slower additions and prolonged unavailable capacity; the downside combines faster additions, route/feedstock restoration, reduced application intensity, and weak affordability. It is possible for nitrogen demand to grow while profitability falls. This is a range model rather than a complete project-status census. [IFA, June 2025, nitrogen balance](https://www.fertilizer.org/wp-content/uploads/2025/07/2025_IFA_Medium_Term_Outlook_Report.pdf).

CF reported 2025 sales of $7.084bn; 2023/24 sales were $6.631bn/$5.936bn. Product-level volume and price inputs, cash flow, depreciation, and capex for all three years are in inputs.json. Its core annual ammonia production capability is 10.485 million short tons, already adjusted for normal outages; upgraded urea/UAN output cannot be added to ammonia as if it were separate nitrogen feedstock. CHS economics are tied to a granular-urea/UAN supply formula, so applying an 11% haircut to the entire company would be wrong. The company consolidates Blue Point despite owning only 40%; common infrastructure is owned separately. These distinctions drive the attributable valuation. [CF 2025 annual report, filed February 25, 2026, printed pp.6,66-70,96-103](https://www.cfindustries.com/globalassets/cf-industries/media/documents/reports/annual-reports/cf-industries-2025-annual-report.pdf).

First-half 2026 revenue was $4.208bn and CFO $1.374bn; adjusted EBITDA included a $170m litigation settlement and therefore cannot simply be annualized as recurring profit. Ammonia/urea/UAN realized prices were $616/$525/$391 per short ton. Management's latest production outlook is 9.5m short tons for 2026, and Yazoo City's restart has moved to the first half of 2027. Base forecasts recover core sold volumes by 2028, then hold material market share approximately constant. Base 2030 ammonia/urea/UAN prices are $450/$365/$275 per short ton; base 2035 prices grow from normalized levels at about inflation. Pricing is my forecast, not guidance. [CF H1 release, August 5, 2026, consolidated results and segment tables](https://ir.cfindustries.com/Investors/news/news-details/2026/CF-Industries-Holdings-Inc--Reports-First-Half-2026-Net-Earnings-of-1-34-Billion-Adjusted-EBITDA-of-2-18-Billion/default.aspx).

Blue Point's disclosed 1.4 Mt annual metric-tonne nameplate and $3.7bn joint project cost plus $550m CF common infrastructure are material, but not the whole business. My attributable base ramps 0.10 Mt in 2029 to 0.45 Mt in 2030 and 0.54 Mt thereafter, versus 0.56 Mt attributable nameplate. Full production is never multiplied by a second utilization adjustment. I assume $650/t starting realization, $400/t operating cost, and a separate full-run-rate $85m annual infrastructure service fee with 65% EBIT margin; actual commercial fee and premium terms are not public, so those economics are unconfirmed. Base 2030 Blue Point product and infrastructure revenue total about $363m, approximately 5.3% of modeled company revenue. Its strategic importance cannot be applied to all of CF. Construction spending is deducted as incurred, including the owned infrastructure. JERA's December 19, 2025 certification under Japan's price-gap support scheme and its Hekinan use case corroborate a funding mechanism; they do not establish CF's eventual project return. [CF project disclosure, accessed September 8](https://www.cfindustries.com/bluepoint); [JERA, December 19, 2025](https://www.jera.co.jp/en/news/information/20251219_2329).

CF's current basic equity capitalization is $20.429bn; modeled diluted shares are 151.638m. Attributable cash is bridged to $1.902bn, including explicit deductions for partner cash and disclosed post-quarter distributions, with $500m reserved for operations. Principal debt is $3.250bn. This gives a $22.277bn attributable operating-asset benchmark; subtracting all bridged cash instead gives $21.777bn. These are not a fully consolidated EV including the market value of CHS and all project partners, which is unavailable. Principal bond maturities are $750m in 2034, $1bn in 2035, $750m in 2043, and $750m in 2044. The undrawn $750m revolver expires September 4, 2030. The filing also disclosed unresolved Blue Point permitting litigation. Core lease expenses stay in operating costs, and operating lease liabilities are not deducted a second time. The $679m unfavorable supply-contract liability is treated through cash economics with noncash revenue amortization removed. [CF Q2 10-Q, August 5, 2026, cover and notes 4,9-12,18-19](https://www.sec.gov/Archives/edgar/data/1324404/000132440426000019/cf-20260630.htm).

The CF DCF uses 24% operating tax; downside/base/upside discount rates are 11%/10%/9.5%, nominal terminal growth 2%, and sustainable terminal ROIC 9%/12%/16%. These required returns reflect commodity exposure and construction risk, not a precisely estimated CAPM. Temporary high margins are allowed to decline through 2035. From 2036 through 2040, nominal sales, costs and depreciation grow 2% with unchanged margins. Net reinvestment converges over five years to the greater of the 2035 net investment burden and g/ROIC of NOPAT. The terminal calculation starts after 2040; it does not discard replacement spending or introduce a sudden 2036 cash-flow drop. The resulting probability-weighted present value is $68.20. Downside/base/upside probabilities are 30%/50%/20%: normalization is the central path because both capital expansion and affordability respond to profits; persistent rents receive a meaningful but minority weight. The downside combines weaker prices, higher gas cost, lower volume, a delayed project, and 20% project capex overrun. A modeled dividend cut to $1 annually from 2028 closes the otherwise approximately $198m cash shortfall. No new shares or debt are required in that path; the remaining downside is economic loss, not an assumed financing rescue.

Present CF fair values are $21.94/$64.52/$146.76 in downside/base/upside; post-2040 terminal value contributes 33.6%/28.2%/30.4% of each scenario EV. Probability-weighted value is $68.20, 49.5% below price. Margin of safety is defined as 1 - price/value and is negative 97.9%. Five-year scenario annualized returns are -22.6%/-6.3%/+10.6%. The XIRR of probability-weighted dated cash flows is -5.0%; the arithmetic probability-weighted scenario IRR is -7.8%, a different statistic. Base 2031 future equity value is $88.66 per share plus the separately dated dividends, not today's $64.52 intrinsic value. Free cash flow retained after debt interest and dividends is included once in future cash; buybacks are neither added as distributions nor assumed to create free accretion.

The current CF price can be justified if base core selling prices from 2027 onward are about 20.0% higher while 2026-35 costs, capex and CHS claims remain fixed, equivalent to 2030 urea around $438/t instead of $365/t. The post-2035 reinvestment transition responds mechanically to higher NOPAT. Allowing CHS's claim to increase with profitability would require a larger gross price increase. Alternatively, a parallel 18.44 percentage-point EBIT-margin increase across the modeled periods justifies price, lifting 2030 attributable EBIT margin from 18.45% to 36.89%. My forecast differs because crop affordability and usable supply normalize faster than permanent scarcity requires. Evidence supporting that difference is the gap between modest nutrient requirements and IFA's capacity additions, plus CF's own costly new capacity. The resulting base value difference is $70.47 per share. These are explicit price-justifying combinations, not a uniquely identified market forecast. Direct current consensus is unavailable.

The strongest opposing case is that low-cost US gas, persistent geopolitical fragmentation, carbon-credit economics, and subsidized ammonia demand support a lasting regional premium while capital costs delay competitors. The upside captures much of that combination and reaches $146.76, 8.7% above price. Historical affordability shocks can sharply reduce applications: IFA discusses the 2008-09 episode. Current food-security policy, changed gas geography, and fixed-cost plants differ, so the analogy sets a stress range rather than forecasting a repeat. Base WACC/g sensitivities span $55.95-$77.13; a five-point margin increase gives $83.62, and a five-point decrease $45.42. Shifting ten probability points from upside to downside lowers weighted value to $55.71. A materially positive case requires evidence of sustained netbacks or much better project returns, not simply more ammonia volume.

Monitor CF's 2027 restart, quarterly realized prices and production gas cost, crop affordability and application volumes, the actual status of nitrogen additions through 2030, and Blue Point cost/ramp disclosures in 2027-29. Repeated urea realization above approximately $440/t after 2028 with little gas-cost increase would challenge the rejection; price below $365/t, continued lost output, and a project overrun together support the downside. A 20% core-price uplift is much more material than shaving a point from WACC. The pending permit case and undisclosed Blue Point commercial terms remain gaps; no favorable outcome is silently assumed to rescue the recommendation.

GSL's chain is: traded-goods growth and longer/less efficient routes [observed/inferred] → liner demand for ship time [observed contracts] → restricted supply of appropriate vessel sizes [external estimate with substitution uncertainty] → charter renewals, utilization and newbuild revenue [partly contracted; later rates assumed] → operating cost, drydock and vessel purchases [observed structure, forecast magnitude] → debt and preferred-adjusted common cash [calculated]. Congestion may migrate from vessels to terminals, inland rail, pilots, crews or repair yards. Owning a leased ship benefits through revenue duration and utilization; its old charters do not instantly reprice with spot scarcity.

At August 5 GSL reported 71 operating vessels, 15 contracted newbuilds costing about $1.33bn, and $3.2bn contracted revenue with 3.3 years' average remaining duration. Charter coverage was 100% for remaining 2026 days and 90% for 2027. Newbuild deliveries run from late 2028 to early 2030, with average firm employment of 7.1 years and over $1bn aggregate contracted EBITDA. H1 cash charter revenue was $384.096m after removing $12.672m noncash charter-liability amortization. Maersk, CMA CGM and Hapag-Lloyd account for approximately 68% of charter revenue together. Strong contracted figures do not erase counterparty concentration or the cost of the ships earning them. [GSL Q2 release, August 5, 2026, fleet, commitments and financial statements](https://globalshiplease.gcs-web.com/news-releases/news-release-details/global-ship-lease-reports-results-second-quarter-2026).

The August presentation's orderbook equals 24.7% of the sub-10,000 TEU fleet versus 39.1% for all sizes. Its low net-growth illustration relies on scrapping every vessel over 25 years old; high charter profits can delay those retirements. These figures originate with MSI and are not independently confirmed capacity records. Maersk's August 13 update supports real approximately 4% 2026 container demand growth and notes congestion, but it is also a liner's estimate and short-term evidence. My base assumes 3.5% annual cargo growth, initially lower required ship time as routing improves, then aging-fleet retirements; new orders induced by profits add supply after 2030. The downside has 1.5% cargo growth, earlier routing improvement, faster delivery, and few early retirements. The upside has 4.5% cargo growth, persistent cycle delays and more retirements, followed by a substantial new-investment response. [GSL presentation, August 5, 2026, industry/orderbook pages](https://globalshiplease.gcs-web.com/static-files/785047b1-1534-4f53-8682-d8ade9d07edf); [Maersk Q2 presentation, August 13, 2026](https://investor.maersk.com/static-files/5b6d7db2-1859-463e-abba-259e202466e4).

The GSL model forecasts existing ships and newbuilds separately. Base average existing ships decline from 71 in 2026 to 58 in 2030 and 22 in 2035. Newbuild average service rises from 0.25 ship in 2028 to 8 in 2029, 14.75 in 2030, and 15 thereafter. Base old-fleet charter rate falls from $30,700/day to $25,000/day in 2030, then grows modestly. Old-fleet operating cost starts at $8,700/calendar day and grows 3%; utilization is 96%. New ships assume $38,000/day, 97% utilization, and starting $10,000 daily operating cost. This yields roughly $140m annual newbuild EBITDA, consistent in order of magnitude with contracted aggregate EBITDA divided by charter years. The 2030 newbuild revenue contribution is about $198m, 28% of company cash revenue. The assumptions are a cohort approximation, not unpublished vessel contracts.

Capex includes all remaining modeled newbuild installments, drydocks and other vessel investment. Growth payments are explicitly concentrated in 2028-30; no fleet replacement is assumed afterward, so the business shrinks. The engine uses a finite $1.076bn 2035 residual in base: 22 old ships at $8m plus 15 newbuilds at $60m, net of assumed selling costs. Downside residual is $615m; upside $1.640bn. These are analyst vessel-price assumptions, not broker appraisals. Using a perpetuity would silently replace old vessels without paying for them. Conversely, this finite model assigns no extra value to future accretive transactions. That is a limitation, not proof management cannot create value.

Historical revenue in 2023/24/25 was $674.8m/$711.1m/$766.5m; full inputs distinguish operating cash, drydock capex, and stock compensation. The 2025 report describes a 2016 ten-year-old ship valuation around $5m versus $64m in 2022, and charter examples ranging from $5,300/day to $102,600/day. High orderbooks and prolonged asset lives have destroyed earlier shortages. Current longer contracts provide more near-term protection, but do not prevent later rate normalization. Related-party management and equity incentive issuance remain governance costs. The 2025 debt maturity schedule included $246.954m in 2027. Our $80m net repayment in that year implies partial refinancing; $100m and $450m net financing in 2028/29 help fund newbuilds. The financing is not a verified commitment, and lower collateral values could impair access. [GSL 2025 Form 20-F, filed March 20, 2026, pp.56-61 and notes 12,15,16](https://www.sec.gov/Archives/edgar/data/1430725/000114036126009637/gsl-20251231.htm).

GSL's basic/diluted equity capitalization is $1.629bn using 36.035434m shares. Bridged cash/time deposits are $476.527m; $75m is reserved. Debt principal is $676.4m, including sale-and-leaseback financing, and preferred principal is $108.980m. The conventional EV using all bridged cash is $1.938bn; the operating-asset benchmark with minimum cash retained is $2.013bn. Preferred dividends of $9.536m annually are deducted from common cash returns, while principal is deducted once from enterprise value. Restricted or structured balances are not assumed excess cash at par. This is conservative; a fully realizable additional $100m would add only $2.78 per share and not close the base gap.

The GSL DCF uses 1% operating tax and 12%/11%/10% discount rates for downside/base/upside, reflecting old-asset risk, liner concentration and financing. Terminal growth is irrelevant because the residual overrides the perpetuity. Probabilities are 30%/50%/20%. Present values are $2.45/$27.66/$59.23; terminal sale proceeds contribute 45.3%/29.5%/26.8% of EV. Weighted present value is $26.41, 41.6% below price; margin of safety is negative 71.2%. Scenario five-year annualized returns are -45.9%/-1.6%/+15.5%. Weighted dated-cash-flow XIRR is -2.1%; the arithmetic weighted scenario IRR is -11.5%. Base future equity is $31.50 per share at September 8, 2031 plus separately dated distributions. The downside future equity can be zero even though cash dividend receipts give an IRR above -100%; it is a solvency/asset-value stress, not a forecast of a literal negative share price.

The current GSL price can be justified if old-fleet realized charter rates from 2028 onward are about $8,303/day above base with other assumptions fixed: approximately $33,303/day in 2030 instead of $25,000/day. The generic reverse DCF instead adds 17.64 percentage points to margins, taking 2030 modeled EBIT margin from 39.85% to 57.49%; sale proceeds remain separately identified and that margin is not a pure recurring shipping metric. My forecast differs because old ships retire and a 24.7% segment orderbook need not be offset by universal age-based scrapping. Evidence supporting that difference is the rapidly enlarged orderbook and the dependence of retirement timing on charter profitability. The resulting base difference in value is $17.55 per share. Direct current consensus is unavailable; neither reverse calculation uniquely identifies what investors believe.

The best opposing case is persistent route disruption, resilient liner balance sheets and older-ship scarcity allowing high profitable renewals, while newbuild contracts improve fleet quality. That is reflected in the $59.23 upside. A 30% higher base vessel residual raises base fair value only to $31.05; 30% lower gives $24.27. A five-point EBIT-margin change gives $22.69-$32.63. WACC of 10%-12% gives $29.94-$25.56. Shifting ten probability points from upside to downside lowers weighted value to $20.73. The combined adverse case uses lower rates/utilization, higher vessel cost and construction spending, lower residual values, and ongoing financing needs together.

Monitor 2027 renewal coverage and daily rates, 2028-30 actual delivery payments and financing, vessel retirements by size rather than fleet age alone, Suez/route-cycle changes, and liner payment quality. Sustained post-2028 existing-fleet rates above roughly $33,000/day without higher costs would challenge the rejection. Rates below $25,000/day, utilization below 94%, failure to refinance 2027 maturities, or newbuild cost overruns support the adverse case. A rule requiring early retirement could benefit surviving ships but destroy the value of GSL's own oldest assets; both effects must be modeled.

Other screens produced useful alternatives but no proven recommendation. Mosaic's Q2 phosphate volume and cash flow were hurt by sulfur cost: forecast third-quarter sulfur was $705/long ton, compared with $522 in Q2, while Q2 free cash flow was negative $153m. This makes sulfur a supplier bottleneck rather than automatic phosphate-producer pricing power. Nutrien's retail and low-cost potash mix diversifies the cycle, but working capital and expansion dilute simple EBITDA yields. ICL's industrial products were $414m of $2.135bn Q2 revenue, approximately 19%; that attractive bromine exposure cannot be assigned to the rest of the company. These are unconfirmed ideas until asset claims, supply economics and full cash models are resolved. [Mosaic, August 4, 2026](https://www.sec.gov/Archives/edgar/data/1285785/000128578526000109/pressreleaseq22026-ex991.htm); [Nutrien, August 5, 2026](https://www.nutrien.com/news/press-releases/nutrien-reports-second-quarter-2026-results-1753); [ICL, August 5, 2026](https://investors.icl-group.com/reports-news-and-events/press-releases/press-releases-details/2026/ICL-Reports-Second-Quarter-2026-Results/default.aspx).

Scorpio's large vessel-sale gains and convertible dilution complicate a superficially low earnings multiple. Teekay Tankers' spot exposure makes route windfalls fragile. Flex LNG's 89% remaining-2026 coverage protects nearer cash flow but does not establish a long-run ship shortage. Cheniere has more contract protection and raised its 2026 outlook; a complete NCI and growth-capex bridge is required before calling it undervalued. Yara and Maersk are non-US leader comparisons with dated primary disclosures but no verified local quote in this feed. Every name has a specific role source and advance/rejection reason in screened.json; none counts solely because it appeared in a list.

Across these chains, prolonged geopolitical disruption is a common positive exposure for nitrogen and vessel rates, while restoration of supply routes is a shared risk. Farmer/consumer affordability, higher financing costs and capital spending overruns can hurt both at once. A stronger business or larger backlog is not sufficient compensation for these dependencies at the observed prices.

Reproduction: run `python reproduce.py` from the project root. The common engine reads inputs.json, computes segment revenue times EBIT margin less corporate cost, applies operating tax, adds depreciation, and deducts capex and working-capital investment. It discounts dated FCFF to September 8, 2026, then adds excess cash and subtracts debt/preferred claims. First-year annual flows are prorated for the remaining calendar-year fraction; seasonality and intra-year financing dates are unresolved. Annual funding sufficiency does not establish that a loan can be drawn before each vessel installment falls due. Remaining 2026 dividends use explicit stub overrides, excluding distributions already paid. Cash remaining after dividends, interest, preferred dividends and financing is retained without interest and counted once in the five-year exit equity. The operational reverse-price result can be reproduced by raising selected segment revenue and EBIT by equal amounts, leaving 2026-35 costs and capex fixed, allowing CF terminal reinvestment to respond to changed NOPAT, and bisecting until fair value equals price. Every forecast number below is an analyst assumption or calculated result unless specifically identified as reported/management/IFA/MSI.

Annual base operating output follows. All amounts are USD millions; the complete three-scenario segment volumes, prices, costs, tax, D&A, capital investment, working capital, dividends and financing are in inputs.json. No terminal scarcity multiple is used.

CF annual base model:

```csv
year,revenue,EBIT,operating_tax_rate,DA,capex,delta_NWC,FCFF
2026,7596.5,2527.3,0.240,800.0,940.0,20.0,1760.7
2027,7244.5,2103.3,0.240,820.0,1200.0,-80.0,1298.5
2028,6681.0,1459.2,0.240,840.0,1300.0,-60.0,709.0
2029,6469.7,1133.6,0.240,865.0,933.0,20.0,773.5
2030,6871.2,1267.5,0.240,895.0,700.0,40.0,1118.3
2031,7076.1,1325.0,0.240,915.0,720.0,30.0,1172.0
2032,7228.3,1359.9,0.240,934.0,740.0,25.0,1202.5
2033,7373.2,1384.4,0.240,953.0,760.0,25.0,1220.2
2034,7518.8,1410.0,0.240,972.0,780.0,25.0,1238.6
2035,7668.7,1437.7,0.240,991.0,800.0,25.0,1258.6
```

CF explicit base normalization, calculated by the common engine; amounts are USD millions:

```csv
year,revenue,EBIT,DA,capex,delta_NWC,FCFF
2036,7822.1,1466.4,1010.8,887.0,25.5,1212.8
2037,7978.5,1495.7,1031.0,977.2,26.0,1164.6
2038,8138.1,1525.6,1051.7,1070.6,26.5,1114.0
2039,8300.8,1556.2,1072.7,1167.4,27.1,1060.9
2040,8466.8,1587.3,1094.1,1267.6,27.6,1005.3
```

GSL annual base model:

```csv
year,revenue,EBIT,operating_tax_rate,DA,capex,delta_NWC,FCFF
2026,763.8,378.4,0.010,120.7,214.7,15.0,265.7
2027,757.9,403.7,0.010,119.0,213.5,0.0,305.2
2028,674.0,312.2,0.010,112.9,342.0,0.0,80.0
2029,694.2,297.8,0.010,126.2,783.7,10.0,-372.6
2030,706.5,281.5,0.010,136.9,159.1,10.0,246.5
2031,639.8,278.4,0.010,124.0,62.0,0.0,337.6
2032,577.1,254.1,0.010,110.4,52.8,0.0,309.2
2033,520.7,225.0,0.010,98.5,44.8,0.0,276.5
2034,461.8,202.0,0.010,86.6,36.7,0.0,249.8
2035,409.9,174.4,0.010,76.4,29.8,0.0,219.2
```

Annual nitrogen balances follow. Capability includes normal achievable operation; availability deducts temporary/geographic restrictions, permanent closures and industrial requirements once. Headroom is available fertilizer nitrogen minus financially supported agricultural purchases, not a claimed change in inventory. The baseline and industrial split are explicitly uncertain.

CF base industry path:

```csv
year,desired_fertilizer_N_Mt,supported_N_Mt,capability_N_Mt,temporary_unavailable_N_Mt,closures_N_Mt,industrial_N_Mt,available_fertilizer_N_Mt,headroom_N_Mt
2026,118.9,118.9,174,13,0,40.0,121.0,2.1
2027,120.084,118.283,178,9,0,40.8,128.2,9.917
2028,121.281,120.432,182,7,0,41.616,133.384,12.952
2029,122.489,122.489,187,6,2,42.448,136.552,14.063
2030,123.709,123.709,191,5,5,43.297,137.703,13.994
2031,124.941,124.941,194,5,7,44.163,137.837,12.896
2032,126.186,126.186,197,5,9,45.046,137.954,11.768
2033,127.442,127.442,200,5,11,45.947,138.053,10.61
2034,128.712,128.712,202,5,13,46.866,137.134,8.422
2035,129.994,129.994,204,5,15,47.804,136.196,6.202
```

CF upside industry path:

```csv
year,desired_fertilizer_N_Mt,supported_N_Mt,capability_N_Mt,temporary_unavailable_N_Mt,closures_N_Mt,industrial_N_Mt,available_fertilizer_N_Mt,headroom_N_Mt
2026,118.9,118.9,174,15,0,40.0,119.0,0.1
2027,120.679,118.266,177,16,0,41.2,119.8,1.534
2028,122.486,121.261,180,14,0,42.436,123.564,2.303
2029,124.319,124.319,184,14,0,43.709,126.291,1.972
2030,126.179,126.179,187,12,0,45.02,129.98,3.8
2031,128.068,128.068,190,11,0,46.371,132.629,4.561
2032,129.984,129.984,193,10,0,47.762,135.238,5.254
2033,131.93,131.93,196,9,0,49.195,137.805,5.875
2034,133.904,133.904,199,8,0,50.671,140.329,6.425
2035,135.908,135.908,202,7,0,52.191,142.809,6.901
```

CF downside industry path:

```csv
year,desired_fertilizer_N_Mt,supported_N_Mt,capability_N_Mt,temporary_unavailable_N_Mt,closures_N_Mt,industrial_N_Mt,available_fertilizer_N_Mt,headroom_N_Mt
2026,118.9,118.9,174,13,0,40.0,121.0,2.1
2027,119.132,113.175,180,5,0,40.4,134.6,21.425
2028,119.365,114.59,187,3,0,40.804,143.196,28.606
2029,119.598,117.206,194,2,0,41.212,150.788,33.582
2030,119.831,119.831,200,2,3,41.624,153.376,33.545
2031,120.065,120.065,204,2,7,42.04,152.96,32.895
2032,120.299,120.299,208,2,12,42.461,151.539,31.24
2033,120.534,120.534,211,2,17,42.885,149.115,28.58
2034,120.769,120.769,214,2,21,43.314,147.686,26.916
2035,121.005,121.005,217,2,25,43.747,146.253,25.247
```

Annual container balances follow. These are normalized TEU-days per 1,000 starting TEU; they do not masquerade as an absolute global fleet census. Demand above usable capacity is unmet desired transport work, and the resulting rate response is modeled separately. The persistent path draws new investment after 2030; the normalization path eases in 2028-30 before aging and cargo growth tighten it again; the oversupply path remains loose despite positive cargo growth.

GSL base industry path:

```csv
year,opening_TEU,additions_TEU,retirements_TEU,closing_TEU,cargo_TEU_moves,cycle_days,required_TEU_days,usable_TEU_days,demand_supply_ratio
2026,1000,0,0,1000,10000.0,35.04,350400.0,350400.0,1.0
2027,1000,45,10,1035,10350.0,34.3392,355410.72,356532.0,0.9969
2028,1035,55,20,1070,10712.25,33.288,356589.38,368796.0,0.9669
2029,1070,65,30,1105,11087.18,33.288,369070.01,381060.0,0.9685
2030,1105,55,40,1120,11475.23,33.288,381987.46,389820.0,0.9799
2031,1120,50,50,1120,11876.86,33.288,395357.02,392448.0,1.0074
2032,1120,70,50,1140,12292.55,33.288,409194.51,395952.0,1.0334
2033,1140,80,50,1170,12722.79,33.288,423516.32,404712.0,1.0465
2034,1170,80,50,1200,13168.09,33.288,438339.39,415224.0,1.0557
2035,1200,80,50,1230,13628.97,33.288,453681.27,425736.0,1.0656
```

GSL upside industry path:

```csv
year,opening_TEU,additions_TEU,retirements_TEU,closing_TEU,cargo_TEU_moves,cycle_days,required_TEU_days,usable_TEU_days,demand_supply_ratio
2026,1000,0,0,1000,10000.0,35.04,350400.0,346750.0,1.0105
2027,1000,35,15,1020,10450.0,35.3904,369829.68,350217.5,1.056
2028,1020,45,25,1040,10920.25,35.7408,390298.47,357152.5,1.0928
2029,1040,55,35,1060,11411.66,35.7408,407861.9,364087.5,1.1202
2030,1060,50,45,1065,11925.19,35.3904,422037.1,368421.88,1.1455
2031,1065,80,50,1095,12461.82,35.04,436662.15,374490.0,1.166
2032,1095,100,50,1145,13022.6,35.04,456311.95,388360.0,1.175
2033,1145,100,50,1195,13608.62,35.04,476845.99,405697.5,1.1754
2034,1195,95,45,1245,14221.01,35.04,498304.05,423035.0,1.1779
2035,1245,95,45,1295,14860.95,35.04,520727.74,440372.5,1.1825
```

GSL downside industry path:

```csv
year,opening_TEU,additions_TEU,retirements_TEU,closing_TEU,cargo_TEU_moves,cycle_days,required_TEU_days,usable_TEU_days,demand_supply_ratio
2026,1000,0,0,1000,10000.0,35.04,350400.0,354050.0,0.9897
2027,1000,50,2,1048,10150.0,32.9376,334316.64,362547.2,0.9221
2028,1048,65,5,1108,10302.25,31.8864,328501.66,381665.9,0.8607
2029,1108,70,10,1168,10456.78,31.8864,333429.19,402908.9,0.8276
2030,1168,65,15,1218,10613.64,31.8864,338430.63,422381.65,0.8012
2031,1218,45,30,1233,10772.84,31.8864,343507.09,433888.27,0.7917
2032,1233,35,45,1223,10934.43,31.8864,348659.69,434773.4,0.8019
2033,1223,30,50,1203,11098.45,31.8864,353889.59,429462.65,0.824
2034,1203,30,50,1183,11264.93,31.8864,359197.93,422381.65,0.8504
2035,1183,30,50,1163,11433.9,31.8864,364585.9,415300.65,0.8779
```

The source register is sources.json, with 20 distinct economic/financial primary disclosures and five raw Massive data groups. Company presentations that reproduce IFA/MSI estimates are labeled as such rather than counted as independent corroboration. Remaining gaps are current interim cash, exact post-quarter repurchases, nitrogen industrial demand and project status, geographic inventory, absolute smaller-ship fleet capacity, confidential charter/project terms, newbuild financing commitments, unpriced restricted assets, and direct consensus. These gaps are material to a positive recommendation. They do not justify inventing missing inputs or treating the two modeled companies as proven bargains.
