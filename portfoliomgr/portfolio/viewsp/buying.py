import logging

from django.shortcuts import render
from moneyed import Decimal

from ..forms import BuyForm
from ..market import get_market_price
from ..models import (
    BUY,
    DRAFT,
    EXECUTED,
    AccountBooking,
    Asset,
    Batch,
    BatchPosition,
    BatchPositionBooking,
    Transaction,
)

logger = logging.getLogger(__name__)
COMP = "...[completed]"  # TODO refactor
STAR = "..."  # TODO refactor


def buy(request):
    def get_description_string(
        security: str, description: str, date, batch_position: int = 0
    ) -> str:
        if batch_position == 0:
            return f"BUY: {security} - {description} - [{date}]"
        else:
            return (
                f"BUY: {security} - {description} - [{date}] - BATCH {batch_position}"
            )

    logger.debug(f"Request method is: {request.method}")
    if request.method == "POST":
        form = BuyForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug("Form is valid")

            # DATA extraction:
            logger.debug(f"Extracting cleaned data from form{STAR}")
            sec = form.cleaned_data["security"]
            depot = form.cleaned_data["depot"]
            bankaccount = form.cleaned_data["bank_account"]
            bdate = form.cleaned_data["buy_date"]
            descr = form.cleaned_data["description"]
            # Position 1
            q1 = form.cleaned_data["quantity_1"]
            price1 = form.cleaned_data["price_1"]
            fee1 = form.cleaned_data["buy_fee_1"]
            yfee1 = form.cleaned_data["yearly_fee_1"]
            c1 = form.cleaned_data["comment_1"]
            # Position 2
            q2 = form.cleaned_data["quantity_2"]
            price2 = form.cleaned_data["price_2"]
            fee2 = form.cleaned_data["buy_fee_2"]
            yfee2 = form.cleaned_data["yearly_fee_2"]
            c2 = form.cleaned_data["comment_2"]
            logger.debug(f"Extracting cleaned data from form{COMP}")

            logger.debug(f"Creating Transaction{STAR}")
            # Eine Transaction anlegen (DRAFT)
            trans = Transaction.objects.create(
                date=bdate,
                description=get_description_string(
                    security=sec, description=descr, date=bdate
                ),
                transaction_type=BUY,
                status=DRAFT,
            )
            logger.debug(f"Creating Transaction...{COMP}")

            logger.debug(f"Handling Asset{STAR}")
            assets = Asset.objects.filter(fk_security=sec, fk_depot=depot)
            if assets:
                asset = assets[0]
            else:
                asset = Asset.objects.create(fk_security=sec, fk_depot=depot)
            logger.debug(f"Handling Asset{COMP}")

            # Einen neuen Batch anlegen
            logger.debug(f"Creating Batch{STAR}")
            batch = Batch.objects.create(
                in_date=bdate,
                fk_asset=asset,
                description=get_description_string(
                    security=sec, description=descr, date=bdate
                ),
            )

            logger.debug(f"Creating Batch{COMP}")

            # Die erste BatchPosition anlegen
            logger.debug(f"Creating BatchPosition 1{STAR}")
            bp1 = BatchPosition.objects.create(
                quantity=q1,
                buy_price=price1,
                buy_fee=fee1,
                yearly_fee=yfee1,
                fk_batch=batch,
                comment=c1,
            )
            logger.debug(f"Creating BatchPosition 1{COMP}")

            # Eine Account Booking anlegen
            logger.debug(f"Creating AccountBooking 1{STAR}")
            ab1 = AccountBooking.objects.create(
                fk_bank_account=bankaccount,
                fk_transaction=trans,
                value=(-1) * ((q1 * fee1.amount) + fee1.amount),
                booking_date=bdate,
                description=get_description_string(
                    security=sec, description=descr, date=bdate, batch_position=1
                ),
            )
            logger.debug(f"Creating AccountBooking 1{COMP}")

            # Eine BatchpositionBooking anlegen
            logger.debug(f"Creating BatchPositionBooking 1{STAR}")
            BatchPositionBooking.objects.create(
                fk_batch_position=bp1,
                fk_transaction=trans,
                quantity=q1,
                booking_date=bdate,
                description=get_description_string(
                    security=sec, description=descr, date=bdate, batch_position=1
                ),
            )
            logger.debug(f"Creating BatchPositionBooking 1{COMP}")

            # Die zweite Batchposition anlegen
            if float(q2 > 0.0):
                logger.debug(f"Creating BatchPosition 2{STAR}")
                bp2 = BatchPosition.objects.create(
                    quantity=q2,
                    buy_price=price2,
                    buy_fee=fee2,
                    yearly_fee=yfee2,
                    fk_batch=batch,
                    comment=c2,
                )
                logger.debug(f"Creating BatchPosition 2{COMP}")

                logger.debug(f"Creating AccountBooking 2{STAR}")
                AccountBooking.objects.create(
                    fk_bank_account=bankaccount,
                    fk_transaction=trans,
                    value=(-1) * ((q2 * fee2.amount) + fee1.amount),
                    booking_date=bdate,
                    description=get_description_string(
                        security=sec, description=descr, date=bdate, batch_position=2
                    ),
                )
                logger.debug(f"Creating AccountBooking 2{COMP}")

                logger.debug(f"Creating BatchPositionBooking 2{STAR}")
                BatchPositionBooking.objects.create(
                    fk_batch_position=bp2,
                    fk_transaction=trans,
                    quantity=q2,
                    booking_date=bdate,
                    description=get_description_string(
                        security=sec, description=descr, date=bdate, batch_position=2
                    ),
                )
                logger.debug(f"Creating BatchPositionBooking 2{COMP}")

            # Transaction Type (EXECUTED)
            logger.debug(f"Saving Transaction{STAR}")
            logger.error("Transaction handling not implemted!!")
            trans.status = EXECUTED
            trans.save()
            logger.debug(f"Saving Transaction{COMP}")

            return render(request, "portfolio/buy_success.html")
        else:
            logger.info("Form is invalid")
            # TODO Add Error Messages
            return render(request, "portfolio/buy.html", {"form": form})

    else:
        form = BuyForm()
        return render(request, "portfolio/buy.html", {"form": form})
