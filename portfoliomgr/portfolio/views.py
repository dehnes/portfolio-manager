import logging
import pprint
from dataclasses import dataclass

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.generic.list import ListView

from .forms import BuyForm, DepositForm, WithdrawForm
from .market import get_market_price
from .models import (
    BUY,
    DEPOSIT,
    DRAFT,
    WITHDRAWAL,
    AccountBooking,
    Asset,
    BankAccount,
    Batch,
    BatchPosition,
    BatchPositionBooking,
    Depot,
    Person,
    Portfolio,
    Security,
    Transaction,
)

logger = logging.getLogger(__name__)


def get_sidebar_context():
    return {"portfolios": Portfolio.objects.all()}


def index(request):
    context = {}
    context["sidebar"] = get_sidebar_context()

    logger.debug("This is a debug message")

    # Get all relevant data
    persons = Person.objects.all()
    securities = Security.objects.all()
    portfolios = Portfolio.objects.all()
    depots = Depot.objects.all()
    assets = Asset.objects.annotate(
        batch_positions_sum=(Sum("batch__batch_positions__quantity")),
    )
    # Calculating the Portfolio Values
    for asset in assets:
        if asset.batch_positions_sum > 0:
            asset.price = get_market_price(asset.fk_security.ticker_symbol)
            asset.balance = float(asset.price) * float(asset.batch_positions_sum)

    for depot in depots:
        depot.balance = 0.0
    for port in portfolios:
        port.balance = 0.0

    for depot in depots:
        for asset in assets:
            if asset.fk_depot == depot:
                depot.balance += asset.balance

    for port in portfolios:
        for depot in depots:
            if depot.fk_portfolio == port:
                port.balance += depot.balance

    context["portfolios"] = portfolios

    for sec in securities:
        sec.price = get_market_price(sec.ticker_symbol)

    context["persons"] = persons
    context["securities"] = securities
    return render(request, "portfolio/index.html", context)


def portfolio(request, id):
    context = {}
    context["sidebar"] = get_sidebar_context()
    port = Portfolio.objects.filter(id=id)[0]
    depots = Depot.objects.filter(fk_portfolio=port)
    assets = Asset.objects.annotate(
        batch_positions_sum=(Sum("batch__batch_positions__quantity")),
    )
    for asset in assets:
        if asset.batch_positions_sum > 0:
            asset.price = get_market_price(asset.fk_security.ticker_symbol)
            asset.balance = float(asset.price) * float(asset.batch_positions_sum)
    for depot in depots:
        depot.balance = 0.0
    for depot in depots:
        for asset in assets:
            if asset.fk_depot == depot:
                depot.balance += asset.balance

    context["port"] = port
    context["depots"] = depots
    context["assets"] = assets

    return render(request, "portfolio/portfolio.html", context)


def portfolios(request):
    context = {}
    context["sidebar"] = get_sidebar_context()

    assets = Asset.objects.annotate(
        batch_positions_sum=(Sum("batch__batch_positions__quantity")),
    )
    portfolios = Portfolio.objects.all()
    depots = Depot.objects.all()
    for asset in assets:
        if asset.batch_positions_sum > 0:
            asset.price = get_market_price(asset.fk_security.ticker_symbol)
            asset.balance = float(asset.price) * float(asset.batch_positions_sum)

    for depot in depots:
        depot.balance = 0.0
    for port in portfolios:
        port.balance = 0.0

    for depot in depots:
        for asset in assets:
            if asset.fk_depot == depot:
                depot.balance += asset.balance

    for port in portfolios:
        for depot in depots:
            if depot.fk_portfolio == port:
                port.balance += depot.balance

    context["portfolios"] = portfolios
    context["depots"] = depots
    context["assets"] = assets

    return render(request, "portfolio/portfolios.html", context)


def deposit(request):
    if request.method == "POST":
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.fk_transaction = Transaction.objects.create()
            form.instance.fk_transaction.description = form.cleaned_data["description"]
            form.instance.fk_transaction.save()
            form.save()
            return render(request, "portfolio/funding_success.html", {"fund": "d"})
        else:
            logger.error("Error: DepositForm is not valid!")
    else:
        form = DepositForm()
    return render(request, "portfolio/deposit.html", {"form": form})


def withdraw(request):
    if request.method == "POST":
        form = WithdrawForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.fk_transaction = Transaction.objects.create()
            form.instance.fk_transaction.description = form.cleaned_data["description"]
            form.instance.fk_transaction.transaction_type = WITHDRAWAL
            form.instance.value = float(form.cleaned_data["value"]) * (-1)
            form.instance.fk_transaction.save()
            form.save()
            return render(request, "portfolio/funding_success.html", {"fund": "w"})

        else:
            logger.error("Error: WithdrawForm is not valid!")
    else:
        form = WithdrawForm()

    return render(request, "portfolio/withdraw.html", {"form": form})


class BankAccountsList(ListView):
    model = BankAccount


def bankaccount(request, id):
    account = BankAccount.objects.filter(id=id)[0]
    bookings = AccountBooking.objects.filter(fk_bank_account=account)
    balance = 0.0
    for booking in bookings:
        balance += float(booking.value)
    return render(
        request,
        "portfolio/bankaccount.html",
        {"account": account, "bookings": bookings, "balance": balance},
    )


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
            q1 = form.cleaned_data["quantity_1"]
            fee1 = form.cleaned_data["buy_fee_1"]
            yfee1 = form.cleaned_data["yearly_fee_1"]
            q2 = form.cleaned_data["quantity_2"]
            fee2 = form.cleaned_data["buy_fee_2"]
            yfee2 = form.cleaned_data["yearly_fee_2"]
            bdate = form.cleaned_data["buy_date"]
            descr = form.cleaned_data["description"]
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
            # Wenn das Asset im Depot noch nicht vorhanden ist, anlegen
            asset = (
                Asset.objects.create()
            )  # FIXME Das asset auswählen, das Asset muss einen combine PK haben, im Model
            logger.debug(f"Handling Asset{COMP}")

            # Einen neuen Batch anlegen
            logger.debug(f"Creating Batch{STAR}")
            batch = Batch.objects.create(in_date=bdate, fk_asset=asset)
            logger.debug(f"Creating Batch{COMP}")

            # Die erste BatchPosition anlegen
            logger.debug(f"Creating BatchPosition 1{STAR}")
            bp1 = BatchPosition.objects.create(
                quantity=q1,
                buy_fee=fee1,
                yearly_fee=yfee1,
                fk_batch=batch,
            )
            logger.debug(f"Creating BatchPosition 1{COMP}")

            # Eine Account Booking anlegen
            logger.debug(f"Creating AccountBooking 1{STAR}")
            ab1 = AccountBooking.objects.create(
                fk_bank_account=form.bank_account,
                fk_transaction=trans,
                value=(-1) * (q1 * fee1),
                booking_date=bdate,
                description=get_description_string(
                    security=sec, description=descr, date=bdate, batch_position=1
                ),
            )
            logger.debug(f"Creating AccountBooking 1{COMP}")

            # Eine BatchpositionBooking anlegen #TODO Create Model
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
                    buy_fee=fee2,
                    yearly_fee=yfee2,
                    fk_batch=batch,
                )
                logger.debug(f"Creating BatchPosition 2{COMP}")

                logger.debug(f"Creating AccountBooking 2{STAR}")
                AccountBooking.objects.create(
                    fk_bank_account=form.bank_account,
                    fk_transaction=trans,
                    value=(-1) * (q2 * fee2),
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
            # TODO implement
            logger.debug(f"Saving Transaction{COMP}")

            return render(request, "buy_success.html")
        else:
            logger.info("Form is invalid")
            # TODO Add Error Messages
            return render(request, "buy.html", {"form": form})

    else:
        form = BuyForm()
        return render(request, "buy.html", {"form": form})
