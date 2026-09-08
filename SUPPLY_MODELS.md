# Annual demand and supply appendix

Research date: September 8, 2026. The tables below expose the operational assumptions behind the company forecasts through 2035. Every future value is an analyst scenario calculation; source-backed starting observations, management targets and unresolved quantities are identified separately. These are not investment recommendations or independently measured capacity censuses.

Demand means financially supported activity where budgets can be modeled, and desired activity where they cannot. Production nameplate, usable output, fulfilled demand and installed asset stocks are distinct. Supply estimates already adjusted for normal availability are not adjusted again. The scenarios are coherent within each value chain; their labels do not assert that all industries experience the same macroeconomic outcome simultaneously.

The cash-flow models separately extend normalized economics through 2040 where needed. Those extra financial normalization years do not add independently measured industry capacity evidence.

## Electrical connections and grid equipment

More electricity consumption requires network connections and replacement equipment, but TWh are not transformer GVA or switchgear units. The calculation starts with 4,200 TWh of 2025 US use. Net growth equals `(1 + gross activity growth) × (1 − efficiency improvement) − 1`; any efficiency-induced extra usage is already inside gross activity, with no second rebound term. Incremental peak GW equals additional annual TWh divided by `8.76 × assumed 60% load factor`. Equipment duty equals peak GW times 1.5 for connections/redundancy plus 20 GW-equivalents of replacements annually. The two conversion factors are assumptions. [EIA, 2025 use, retrieved September 8, 2026; exact update date unavailable](https://www.eia.gov/energyexplained/electricity/use-of-electricity.php)

Usable equipment supply is measured in the same standardized connection-duty GW-equivalents. Its level is unverified: there is no industry census in these inputs. An Eaton/Fibrebond $242 m-plus plant expansion supports the direction of competitive response, not these output levels or a qualification date. Supplier content per connection and individual customers' financed deployment schedules remain unresolved. [Eaton, September 2, 2026, expansion announcement](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-expands-manufacturing-for-modular-electrical-enclosures.html)

**Orderly-normalization annual scenario. All supply levels are assumptions.**

| Year | US use TWh | New peak GW | Equipment demand GW-eq | Usable supply GW-eq | Demand / supply |
| ---- | ---------- | ----------- | ---------------------- | ------------------- | --------------- |
| 2026 | 4,324.3    | 23.6        | 55.5                   | 53.0                | 1.05            |
| 2027 | 4,452.3    | 24.4        | 56.5                   | 60.0                | 0.94            |
| 2028 | 4,575.3    | 23.4        | 55.1                   | 69.0                | 0.80            |
| 2029 | 4,688.1    | 21.5        | 52.2                   | 79.0                | 0.66            |
| 2030 | 4,794.4    | 20.2        | 50.3                   | 87.0                | 0.58            |
| 2031 | 4,888.8    | 18.0        | 47.0                   | 93.0                | 0.50            |
| 2032 | 4,975.4    | 16.5        | 44.7                   | 98.0                | 0.46            |
| 2033 | 5,058.7    | 15.8        | 43.8                   | 102.0               | 0.43            |
| 2034 | 5,138.3    | 15.2        | 42.7                   | 106.0               | 0.40            |
| 2035 | 5,214.1    | 14.4        | 41.6                   | 110.0               | 0.38            |

Even the scenario named persistent scarcity clears this conditional aggregate equipment deficit around 2029; it does not assume that every constraint persists. A more specific skilled-labor, qualification or product-mix constraint could outlast it, but the evidence does not establish the dates. The volume opportunity is therefore separated from an unproven perpetual pricing premium. [Inputs, formulas and all three paths](research/power_water/demand_supply.json)

## Water mains, valves and field installation

Annual renewal miles equal beginning installed mains times the renewal rate. New miles equal housing starts times 0.004 assumed miles per home. Renewal does not enlarge the installed stock; only new miles do. The 2.2 m-mile starting stock is a stale ASCE 2021 estimate reproduced by EPA, not an independent EPA census; the 0.5% renewal anchor comes from a 2018 EPA report and is explicitly historical. [EPA, October 2025 page, citing ASCE](https://www.epa.gov/emergency-response-research/stormwater-management-technologies-hydrant-flushing-chlorination), [EPA, March 2018, p 24](https://www.epa.gov/sites/default/files/2018-10/documents/corrected_sixth_drinking_water_infrastructure_needs_survey_and_assessment.pdf)

Usable annual installation capacity is jointly constrained by crews, equipment, approvals and budgets. It is not claimed valve-foundry capacity. Completed work is the minimum of desired miles, usable installation miles and funded miles. The budget assumption is $21 bn in 2026 rising 3% annually, at $1 m per completed mile. A six-valves-per-mile assumption is illustrative product intensity, not Mueller's market size or captured revenue. National infrastructure need is not treated as a funded purchase order.

**Orderly-normalization annual scenario. Miles are thousands; capacity and budget are assumptions.**

| Year | Renewal miles k | New miles k | Desired miles k | Usable miles k | Budget $bn | Completed miles k |
| ---- | --------------- | ----------- | --------------- | -------------- | ---------- | ----------------- |
| 2026 | 11.00           | 5.20        | 16.20           | 19.00          | 21.00      | 16.20             |
| 2027 | 11.47           | 5.40        | 16.87           | 20.50          | 21.63      | 16.87             |
| 2028 | 11.94           | 5.60        | 17.54           | 22.00          | 22.28      | 17.54             |
| 2029 | 12.41           | 5.72        | 18.13           | 23.50          | 22.95      | 18.13             |
| 2030 | 12.89           | 5.80        | 18.69           | 25.00          | 23.64      | 18.69             |
| 2031 | 13.37           | 5.84        | 19.21           | 26.00          | 24.34      | 19.21             |
| 2032 | 13.85           | 5.88        | 19.73           | 27.00          | 25.07      | 19.73             |
| 2033 | 14.33           | 5.92        | 20.25           | 28.00          | 25.83      | 20.25             |
| 2034 | 14.82           | 5.96        | 20.78           | 29.00          | 26.60      | 20.78             |
| 2035 | 15.31           | 6.00        | 21.31           | 30.00          | 27.40      | 21.31             |

In the faster-renewal scenario, financial capacity becomes limiting after field crews expand. The binding requirement migrates from installation availability toward ratepayer/customer budgets. This is a reason to model actual completion rather than capitalize the entire infrastructure backlog. [All annual water paths](research/power_water/demand_supply.json)

## Aircraft fleets and maintenance

Passenger/cargo traffic creates seat, flight-hour and cycle demand. Normal fleet need grows by `(1 + traffic growth)/(1 + 1% seats-per-aircraft efficiency)`. Usable active fleet adds qualified deliveries and storage reactivations, less retirements. Annual new-aircraft demand separates fleet growth from replacements. No extra load-factor credit is applied: the opening effective shortage already recognizes unusual utilization/load factors. IATA estimates 30,407 active aircraft versus 33,577 normal requirement in May 2026; the effective 3,170 shortage differs from 5,600 hypothetical missing historical deliveries. [IATA, June 2026, pp 27–29](https://www.iata.org/en/iata-repository/publications/economic-reports/global-outlook-for-air-transport-june-2026/)

2026 starts May 31 and includes seven remaining months. The table's delivery column is the annual usable run rate; only 7/12 enters the 2026 stock bridge. Airbus/Boeing production targets inform plausible additions but remain subject to certification, staffing, engine and component ramps. Geography and aircraft/engine mix prevent perfect interchangeability. [Airbus H1, July 29](https://www.airbus.com/en/newsroom/press-releases/2026-07-airbus-reports-half-year-h1-2026-results), [Boeing Q2, July 28](https://investors.boeing.com/investors/news/press-release-details/2026/Boeing-Reports-Second-Quarter-Results/default.aspx)

**Orderly-normalization annual scenario. Aircraft are units; positive gap indicates shortage.**

| Year | Traffic growth | Normal fleet need | Usable active fleet | Annual usable deliveries | Effective gap |
| ---- | -------------- | ----------------- | ------------------- | ------------------------ | ------------- |
| 2026 | 2.1%           | 33,790            | 31,133              | 1,794                    | 2,657         |
| 2027 | 4.0%           | 34,793            | 32,733              | 2,200                    | 2,061         |
| 2028 | 4.0%           | 35,827            | 34,458              | 2,450                    | 1,369         |
| 2029 | 4.0%           | 36,891            | 36,208              | 2,600                    | 683           |
| 2030 | 4.0%           | 37,987            | 37,883              | 2,650                    | 104           |
| 2031 | 4.0%           | 39,115            | 39,433              | 2,650                    | -317          |
| 2032 | 4.0%           | 40,277            | 40,933              | 2,650                    | -656          |
| 2033 | 4.0%           | 41,473            | 42,333              | 2,600                    | -859          |
| 2034 | 4.0%           | 42,705            | 43,633              | 2,550                    | -927          |
| 2035 | 4.0%           | 43,974            | 44,883              | 2,550                    | -909          |

The base effective gap closes in 2031; the faster-supply/softer-demand path reaches spare capacity in 2028 even though traffic is growing. Persistent delivery constraints instead increase the deficit through 2035. A shortage can migrate to engine repair and qualified parts while aggregate airframe availability improves. Airlines' thin margins constrain financially supported rent increases; no global shortage is assigned immediately to all fixed leases. [All three annual paths, including nameplate, realization, retirements and storage](research/aviation_health/aviation_demand_supply.csv)

## Clinical research services

Annual trial starts are flows; active trials are overlapping cohorts. Standardized annual service-years use current/prior cohort weights 0.5/1.0/0.75/0.25. Outsourced work equals those service-years times outsource share times complexity divided by efficiency. The 2023 and 2024 starts of 5,302 and 5,318 are reported; the 2025 calibration of 5,200 is assumed because the accessible 2026 summary does not expose a verified aggregate. [IQVIA, March 2025, pp 14–15, primary authored report mirror](https://makingpharmaindustry.it/wp-content/uploads/2025/03/iqvia-institute-rd-trends-2025-forweb.pdf), [IQVIA, March 25, 2026 summary](https://www.iqvia.com/insights/the-iqvia-institute/reports-and-publications/reports/global-r-and-d-trends-2026)

Global qualified capacity is unavailable. The initial 8,000 standardized-service-year supply anchor, expansion, outsourcing shares and $5 m service-year fee are scenario assumptions. The budget shown is a calibrated service envelope, not observed sponsor funding or the entire global market. Base trial-start growth is 3%, complexity 2%, efficiency 1% and annual price 2%. The adverse case has efficiency reducing work faster than activity expands. More than 100% utilization indicates unfulfilled work or needed expansion, not immediately realizable supplier revenue.

**Orderly-normalization annual scenario. Work and supply are standardized service-years.**

| Year | New trial starts | Active service-years | Outsourced work | Usable supply assumed | Demand / supply | Budget envelope $bn |
| ---- | ---------------- | -------------------- | --------------- | --------------------- | --------------- | ------------------- |
| 2026 | 5,356            | 13,192               | 7,651           | 8,240                 | 0.93            | 38.3                |
| 2027 | 5,517            | 13,344               | 7,883           | 8,487                 | 0.93            | 40.2                |
| 2028 | 5,682            | 13,675               | 8,229           | 8,742                 | 0.94            | 42.8                |
| 2029 | 5,853            | 14,085               | 8,632           | 9,004                 | 0.96            | 45.8                |
| 2030 | 6,028            | 14,508               | 9,054           | 9,274                 | 0.98            | 49.0                |
| 2031 | 6,209            | 14,943               | 9,497           | 9,552                 | 0.99            | 52.4                |
| 2032 | 6,395            | 15,391               | 9,960           | 9,839                 | 1.01            | 56.1                |
| 2033 | 6,587            | 15,853               | 10,446          | 10,134                | 1.03            | 60.0                |
| 2034 | 6,785            | 16,328               | 10,954          | 10,438                | 1.05            | 64.2                |
| 2035 | 6,988            | 16,818               | 11,394          | 10,751                | 1.06            | 68.1                |

The model is sufficient to expose how starts, duration, outsourcing and efficiency interact; it is insufficient to establish an observed CRO bottleneck. Historical starts after 2021 show that service supply can overshoot while long-run pharmaceutical development continues. [All three clinical paths](research/aviation_health/clinical_demand_supply.csv)

## Nitrogen fertilizer and industrial ammonia

Contained nitrogen is the common unit; tonnes of ammonia, urea and UAN are not added without conversion. Desired fertilizer use equals a crop-activity proxy times nitrogen intensity. The proxy starts at FAO's 2,965 m tonnes of cereal utilization, with noncereal crop mix held proportionate; it does not mean all fertilizer serves cereals. Affordability reduces desired demand to supported demand. [FAO, September 4, 2026, utilization](https://www.fao.org/worldfoodsituation/csdb)

Available fertilizer nitrogen equals productive capability less temporary/geographical outages, economic closures and industrial nitrogen use. Capability already includes normal achievable utilization, so no second yield or utilization discount is applied. IFA's 2024 capability of 166.6 Mt and forecast 17 Mt increase over 2026–30 anchor the assumed 174 Mt 2026 capability. Industrial use of 40 Mt has a 35–45 Mt uncertainty range. Crop years are mapped approximately to calendar years. Project-by-project financing/ramp status and global inventories remain unverified. [IFA, June 2025, nitrogen balance](https://www.fertilizer.org/wp-content/uploads/2025/07/2025_IFA_Medium_Term_Outlook_Report.pdf), [IFA, May 19, 2026, pp 11–12 and 19–26](https://www.fertilizer.org/wp-content/uploads/2026/05/2026_IFA_Medium_Term_Outlook_Report_English.pdf)

**Orderly-normalization annual scenario. Mt of contained nitrogen except cereal activity.**

| Year | Cereal proxy Mt | Supported fertilizer N | Productive capability N | Industrial N | Available fertilizer N | Headroom N |
| ---- | --------------- | ---------------------- | ----------------------- | ------------ | ---------------------- | ---------- |
| 2026 | 2,965           | 118.9                  | 174.0                   | 40.0         | 121.0                  | 2.1        |
| 2027 | 3,004           | 118.3                  | 178.0                   | 40.8         | 128.2                  | 9.9        |
| 2028 | 3,043           | 120.4                  | 182.0                   | 41.6         | 133.4                  | 13.0       |
| 2029 | 3,082           | 122.5                  | 187.0                   | 42.4         | 136.6                  | 14.1       |
| 2030 | 3,122           | 123.7                  | 191.0                   | 43.3         | 137.7                  | 14.0       |
| 2031 | 3,163           | 124.9                  | 194.0                   | 44.2         | 137.8                  | 12.9       |
| 2032 | 3,204           | 126.2                  | 197.0                   | 45.0         | 138.0                  | 11.8       |
| 2033 | 3,246           | 127.4                  | 200.0                   | 45.9         | 138.1                  | 10.6       |
| 2034 | 3,288           | 128.7                  | 202.0                   | 46.9         | 137.1                  | 8.4        |
| 2035 | 3,331           | 130.0                  | 204.0                   | 47.8         | 136.2                  | 6.2        |

This model primarily supports a regional input-cost advantage rather than unavoidable global physical scarcity. Gas prices, plant closures, transport and trade restrictions can let a low-cost producer capture cash while overall capability exceeds supported demand. High margins induce both additions and delayed closures; the oversupply path tests that response. [Nitrogen formulas and all three paths in CF demand_supply](research/agri_transport/inputs.json)

## Regional containership capacity

The modeled segment is below 10,000 TEU, normalized to 1,000 beginning productive TEU. This is not an absolute world-fleet census. Required work equals representative annual cargo TEU moves times voyage/cycle days. Usable supply equals average installed TEU times 365 times technical availability. Cargo growth, voyage duration, ordinary utilization and technical availability are distinct; utilization is the resulting ratio, not a second capacity haircut.

GSL's August presentation reproduces MSI's 24.7% sub-10,000-TEU orderbook/fleet estimate. It is one external estimate carried in an issuer source, not independent corroboration. Maersk's approximately 4% cargo-growth guidance supplies a direct charterer cross-check. Individual ship financing/yard status and the complete segment fleet remain unverified. Deliveries after 2030 include assumed orders induced by higher profits, not already announced contracts. [GSL, August 5, slides 13–16 and 27](https://globalshiplease.gcs-web.com/static-files/785047b1-1534-4f53-8682-d8ade9d07edf), [Maersk, August 13, slide 4](https://investor.maersk.com/static-files/5b6d7db2-1859-463f-a152-07ad65ced1c6)

**Orderly-normalization annual scenario. TEU-days are thousands per 1,000 starting TEU.**

| Year | Delivered TEU | Retired TEU | Closing fleet TEU | Required TEU-days k | Usable TEU-days k | Demand / supply |
| ---- | ------------- | ----------- | ----------------- | ------------------- | ----------------- | --------------- |
| 2026 | 0             | 0           | 1000              | 350.4               | 350.4             | 1.00            |
| 2027 | 45            | 10          | 1035              | 355.4               | 356.5             | 1.00            |
| 2028 | 55            | 20          | 1070              | 356.6               | 368.8             | 0.97            |
| 2029 | 65            | 30          | 1105              | 369.1               | 381.1             | 0.97            |
| 2030 | 55            | 40          | 1120              | 382.0               | 389.8             | 0.98            |
| 2031 | 50            | 50          | 1120              | 395.4               | 392.4             | 1.01            |
| 2032 | 70            | 50          | 1140              | 409.2               | 396.0             | 1.03            |
| 2033 | 80            | 50          | 1170              | 423.5               | 404.7             | 1.05            |
| 2034 | 80            | 50          | 1200              | 438.3               | 415.2             | 1.06            |
| 2035 | 80            | 50          | 1230              | 453.7               | 425.7             | 1.07            |

Shorter routes release effective ship capacity without a single extra newbuild. Larger ships may cascade into smaller-vessel trades; scrapping assumptions cannot be inferred merely from age. The base is loose in 2028–30 and tightens modestly after 2031; demand above supply is unfulfilled work. The downside combines faster deliveries and lower route duration with weak cargo growth. [Container formulas and all three paths in GSL demand_supply](research/agri_transport/inputs.json)

## Scenario comparison: demand relative to usable supply

A ratio above one means modeled demand exceeds usable supply. A ratio below one means modeled spare capacity, not guaranteed price declines or interchangeable local supply. Every grid, water and clinical absolute supply level is an assumption. Aviation ratios compare fleet stocks; other columns compare annual output/work, so these ratios must not be aggregated. Nitrogen uses financially supported demand; water uses desired work before the separate budget limit.

### Persistent scarcity / supplier upside

| Year | Grid D/S assumed | Water D/S assumed | Aircraft fleet D/S | Clinical D/S assumed | Nitrogen D/S | Containership D/S |
| ---- | ---------------- | ----------------- | ------------------ | -------------------- | ------------ | ----------------- |
| 2026 | 1.20             | 0.98              | 1.10               | 0.93                 | 1.00         | 1.01              |
| 2027 | 1.25             | 1.01              | 1.11               | 0.94                 | 0.99         | 1.06              |
| 2028 | 1.16             | 1.03              | 1.11               | 0.97                 | 0.98         | 1.09              |
| 2029 | 0.97             | 1.02              | 1.12               | 1.01                 | 0.98         | 1.12              |
| 2030 | 0.81             | 1.02              | 1.13               | 1.05                 | 0.97         | 1.15              |
| 2031 | 0.67             | 1.01              | 1.13               | 1.09                 | 0.97         | 1.17              |
| 2032 | 0.55             | 1.00              | 1.14               | 1.13                 | 0.96         | 1.18              |
| 2033 | 0.46             | 0.96              | 1.14               | 1.17                 | 0.96         | 1.18              |
| 2034 | 0.44             | 0.93              | 1.15               | 1.21                 | 0.95         | 1.18              |
| 2035 | 0.43             | 0.90              | 1.16               | 1.24                 | 0.95         | 1.18              |

### Orderly normalization / base

| Year | Grid D/S assumed | Water D/S assumed | Aircraft fleet D/S | Clinical D/S assumed | Nitrogen D/S | Containership D/S |
| ---- | ---------------- | ----------------- | ------------------ | -------------------- | ------------ | ----------------- |
| 2026 | 1.05             | 0.85              | 1.09               | 0.93                 | 0.98         | 1.00              |
| 2027 | 0.94             | 0.82              | 1.06               | 0.93                 | 0.92         | 1.00              |
| 2028 | 0.80             | 0.80              | 1.04               | 0.94                 | 0.90         | 0.97              |
| 2029 | 0.66             | 0.77              | 1.02               | 0.96                 | 0.90         | 0.97              |
| 2030 | 0.58             | 0.75              | 1.00               | 0.98                 | 0.90         | 0.98              |
| 2031 | 0.50             | 0.74              | 0.99               | 0.99                 | 0.91         | 1.01              |
| 2032 | 0.46             | 0.73              | 0.98               | 1.01                 | 0.91         | 1.03              |
| 2033 | 0.43             | 0.72              | 0.98               | 1.03                 | 0.92         | 1.05              |
| 2034 | 0.40             | 0.72              | 0.98               | 1.05                 | 0.94         | 1.06              |
| 2035 | 0.38             | 0.71              | 0.98               | 1.06                 | 0.95         | 1.07              |

### Oversupply or demand disappointment

| Year | Grid D/S assumed | Water D/S assumed | Aircraft fleet D/S | Clinical D/S assumed | Nitrogen D/S | Containership D/S |
| ---- | ---------------- | ----------------- | ------------------ | -------------------- | ------------ | ----------------- |
| 2026 | 0.71             | 0.78              | 1.08               | 0.93                 | 0.98         | 0.99              |
| 2027 | 0.41             | 0.65              | 1.02               | 0.89                 | 0.84         | 0.92              |
| 2028 | 0.37             | 0.61              | 0.98               | 0.86                 | 0.80         | 0.86              |
| 2029 | 0.39             | 0.59              | 0.96               | 0.83                 | 0.78         | 0.83              |
| 2030 | 0.36             | 0.57              | 0.94               | 0.80                 | 0.78         | 0.80              |
| 2031 | 0.35             | 0.58              | 0.93               | 0.77                 | 0.78         | 0.79              |
| 2032 | 0.35             | 0.60              | 0.92               | 0.75                 | 0.79         | 0.80              |
| 2033 | 0.34             | 0.59              | 0.92               | 0.72                 | 0.81         | 0.82              |
| 2034 | 0.34             | 0.60              | 0.91               | 0.70                 | 0.82         | 0.85              |
| 2035 | 0.33             | 0.59              | 0.91               | 0.67                 | 0.83         | 0.88              |

## Payments: transaction growth versus fee capture

The requirement is reliable acceptance, settlement, fraud prevention and financing of commerce. No observed processing shortage is assumed. PayPal demand is active accounts times transactions per account times ticket size; revenue is payment volume times fee yield plus other value-added services. Merchant transactions and service revenues are not both treated as new end-customer spending. Fiserv's merchant GPV starts from a reported $4.6 tr in 2025; its all-in revenue/GPV ratio includes software and services and is not a posted card fee. Fiserv's reported throughput benchmark is not annual qualified national capacity. [PayPal, July 28 Form 10-Q, operating metrics](https://www.sec.gov/Archives/edgar/data/1633917/000163391726000082/pypl-20260630.htm), [Fiserv, May 15 investor day, pp 5–9](https://investors.fiserv.com/static-files/af17ec6f-4ca7-4261-804c-2fb24b9d2430)

Customer spending is cross-checked against Census e-commerce, while competitor Adyen's H1 volume growth exceeding revenue growth demonstrates that more transactions need not preserve fees. These datasets are not added to one another. [Census, August 18 Q2 release](https://www.census.gov/retail/ecommerce.html), [Adyen, August 13 H1 results](https://www.adyen.com/press-and-media/adyen-publishes-h1-2026-financial-results-3wjne)

**Base annual scenario. Payment volumes are USD trillions; fee yields are basis points.**

| Year | PayPal accounts m | Transactions/account | PayPal TPV $tr | PayPal fee bp | Fiserv GPV $tr | Fiserv all-in yield bp |
| ---- | ----------------- | -------------------- | -------------- | ------------- | -------------- | ---------------------- |
| 2026 | 440.0             | 62.0                 | 1.98           | 159.0         | 4.88           | 20.9                   |
| 2027 | 442.2             | 64.5                 | 2.11           | 156.3         | 5.14           | 20.4                   |
| 2028 | 446.6             | 67.1                 | 2.26           | 153.6         | 5.43           | 20.3                   |
| 2029 | 451.1             | 69.4                 | 2.41           | 151.0         | 5.73           | 20.2                   |
| 2030 | 455.6             | 71.5                 | 2.56           | 148.5         | 6.04           | 20.0                   |
| 2031 | 457.9             | 73.6                 | 2.70           | 145.9         | 6.37           | 19.8                   |
| 2032 | 460.2             | 75.5                 | 2.84           | 143.5         | 6.72           | 19.4                   |
| 2033 | 462.5             | 77.4                 | 2.98           | 141.0         | 7.09           | 18.9                   |
| 2034 | 464.8             | 78.9                 | 3.12           | 138.6         | 7.48           | 18.5                   |
| 2035 | 467.1             | 80.5                 | 3.26           | 136.3         | 7.89           | 18.0                   |

The downside allows growing transaction intensity alongside declining accounts and fees; the upside requires better retention and stronger monetization. These are fee-capture scenarios, not fabricated capacity ratios. Financial Solutions account/transaction counts are not disclosed, so that segment remains a fee-equivalent sensitivity and prevents a confirmed operating thesis. [All three payment paths](research/payments/demand_supply.json)

## Connectivity and entertainment

Broadband revenue equals average subscribers times monthly realized revenue times twelve; wireless and Peacock use the same customer-stock identity with their own fees. Annual average customers are not annual gross additions. Video decline, advertising and other services are modeled separately. Comcast's Q2 primary disclosures anchor the starting services, while competing fiber, cable and fixed-wireless investment tests retention and pricing. AT&T's greater-than-60 m fiber-location target for 2030 is management guidance, not a completed competing network. [Comcast, July 23 Q2 results](https://www.cmcsa.com/node/45906), [AT&T, July 22, outlook](https://www.sec.gov/Archives/edgar/data/732717/000073271726000294/t-2q2026exhibit991.htm)

Homes passed measure address reach, not simultaneous network throughput. Customer penetration is not capacity utilization. Local competing fiber overlap, fixed-wireless capacity and traffic per household are unavailable; national competitor targets are not summed into Comcast's local supply. No scarcity premium is assigned. The investment case instead depends on whether customer losses and price competition cost less cash than the current valuation implies.

**Base annual scenario. Customers and assumed passings in millions; monthly fees in USD.**

| Year | Broadband customers | Monthly broadband fee | Wireless lines | Monthly wireless fee | Peacock paid customers | Assumed passings |
| ---- | ------------------- | --------------------- | -------------- | -------------------- | ---------------------- | ---------------- |
| 2026 | 28.50               | 74.00                 | 10.15          | 33.00                | 47.0                   | 59.95            |
| 2027 | 27.95               | 72.50                 | 11.90          | 33.00                | 50.0                   | 61.00            |
| 2028 | 27.40               | 72.50                 | 13.60          | 33.50                | 53.0                   | 62.05            |
| 2029 | 26.95               | 73.20                 | 15.10          | 34.00                | 56.0                   | 63.10            |
| 2030 | 26.60               | 74.30                 | 16.40          | 34.50                | 59.0                   | 64.15            |
| 2031 | 26.40               | 75.70                 | 17.50          | 35.00                | 62.0                   | 65.20            |
| 2032 | 26.25               | 77.20                 | 18.40          | 35.20                | 64.0                   | 66.25            |
| 2033 | 26.20               | 78.70                 | 19.20          | 35.50                | 66.0                   | 67.30            |
| 2034 | 26.20               | 80.30                 | 19.90          | 35.70                | 68.0                   | 68.35            |
| 2035 | 26.20               | 82.00                 | 20.50          | 36.00                | 70.0                   | 69.40            |

The adverse path combines faster broadband customer loss, lower realized fees and weak entertainment monetization. The upside requires successful bundles and stronger paid streaming conversion, while continuing network/content investment. Physical demand can expand while a particular provider loses customers and prices. [All three annual connectivity paths](research/connectivity/operating_drivers.json)

## What these models establish and what remains incomplete

The strongest supply evidence is observed fleet/capability and issuer-specific contracted activity, followed by dated manufacturer/project disclosures. Aggregate switchgear, field installation and qualified clinical capacity are much less observable. Normalized container units diagnose the cycle but do not constitute a global ship census. The research therefore does not claim complete project-level financed/under-construction/qualified additions across all chains.

High-profits supply responses, efficiency, replacement and financially supported demand are explicit. They often weaken a headline bottleneck thesis: aircraft availability normalizes; route shortening releases ships; fertilizer capability can expand faster than funded application; grid supply can catch annual connection requirements; water funding limits completion; and clinical efficiency can lower billable work. Payments and connectivity rely on customer retention, cost and pricing economics rather than a demonstrated physical shortage. Source registers and remaining company-specific gaps appear in [SOURCE_REGISTER.md](SOURCE_REGISTER.md) and the linked research inputs.

The expanded value search added responsive-supply cases rather than a new verified physical shortage. [Commerce and retail annual drivers](research/deep_global/operating_drivers.json), [automotive and nylon supply/demand paths](research/deep_cyclicals/demand_supply.json), [browser and sports-data operating drivers](research/deep_neglected/operating_drivers.json), and [footwear demand indices](research/deep_consumer/demand_inputs.json) accompany the seven new valuations. These files distinguish measured starting observations from analyst indices and unreported capacity. The final investment ranking is in [REPORT.md](REPORT.md).
