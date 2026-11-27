# Order sheet: LSN-A-0001 x 2, build B001

Date 2026-11-27. From the BOM `bom.csv` of LSN-A-0001. Prices before tax; CAD totals use rates.csv.

## Summary

- **Purchase reqs to send: 1** (one per supplier)
- **To order:** CA$120.12 before tax
- **From stock:** 5 parts; **made in house:** 2 parts; **extras on these reqs (not for LSN-A-0001):** 1 line

| Req | Supplier | Lines | Total | Total CAD |
|---|---|---|---|---|
| 1 | Mouser | 5 | CAD 120.12 | 120.12 |

## Req 1: Mouser

Upload file for the purchase req: `mouser-2026-11-27.csv`

| PN | Item | Supplier part | Qty to order | For | Price each | Line total | Link |
|---|---|---|---|---|---|---|---|
| ECM-0001 | BME280 temperature, humidity and pressure sensor board, Qwiic | 474-SEN-15440 | 2 | LSN-A-0001 B001 2 | CAD 24.41 | CAD 48.82 | https://www.mouser.ca/ProductDetail/474-SEN-15440 |
| ECM-0002 | SGP40 VOC air quality sensor board, STEMMA QT / Qwiic | 485-4829 | 2 | LSN-A-0001 B001 2 | CAD 21.53 | CAD 43.06 | https://www.mouser.ca/ProductDetail/485-4829 |
| ECM-0003 | Qwiic SHIM for Raspberry Pi, push-fit on GPIO header, no soldering | 474-DEV-15794 | 2 | LSN-A-0001 B001 2 | CAD 2.81 | CAD 5.62 | https://www.mouser.ca/ProductDetail/474-DEV-15794 |
| ECW-0001 | Qwiic / STEMMA QT cable, JST SH 4-pin, 100 mm | 485-4210 | 4 | LSN-A-0001 B001 4 | CAD 1.37 | CAD 5.48 | https://www.mouser.ca/ProductDetail/485-4210 |
| ECM-0005 | AS5600 magnetic angle sensor board, STEMMA QT / Qwiic | 485-6357 | 2 | inventory 2 | CAD 8.57 | CAD 17.14 | https://www.mouser.ca/ProductDetail/485-6357 |
| | **Total** | | | | | **CAD 120.12** | |

Split by purpose: LSN-A-0001 B001 CAD 102.98; inventory CAD 17.14

## From stock (count before the build)

| PN | Part | Needed | On hand | Still to order | Must be exactly this part |
|---|---|---|---|---|---|
| ECM-0004 | Raspberry Pi Zero 2 W with header (pre-soldered GPIO) | 2 | 2 | 0 | yes: SC0721 |
| ECP-0001 | Wall power supply, 5.1 V 2.5 A, USB Micro-B, UL listed, 100-240 VAC | 2 | 2 | 0 | yes: 1260 |
| ECX-0001 | microSD card, SanDisk Extreme 64 GB microSDXC A2 | 2 | 2 | 0 | no: any matching part |
| HWB-0036 | Screw, M2 x 5 mm, pan head Phillips, nylon, black | 16 | 16 | 0 | no: any matching part |
| HWN-0006 | Heat-set insert, M2, brass | 16 | 16 | 0 | yes: M20X100C |

## Made in house

| PN | Part | Quantity |
|---|---|---|
| LSN-0001 | Housing base, 3D printed | 2 |
| LSN-0002 | Housing lid, 3D printed | 2 |

## Check before sending

- [ ] Number of units is right.
- [ ] Stock counted, and stock of an exact part is that exact part.
- [ ] Each link opens the right part, in stock.
- [ ] Quantities and packs are right; nothing ordered twice.
