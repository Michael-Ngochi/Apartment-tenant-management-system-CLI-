import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "lib")))

import click
from db import SessionLocal
from models.block import Block
from models.unit import Unit
from models.tenant import Tenant
from models.payment import Payment

# List of available actions
ACTIONS = [
    "Add Block", "List Blocks",
    "Add Unit", "List Vacant Units",
    "Add Tenant", "List Tenants","Vacate Tenant",
    "Add Payment", "List Payments","Check Pending Payments",
    "Exit"
]

def display_menu():
    click.echo("\n=== Apartment Management Menu ===")
    for i, action in enumerate(ACTIONS, start=1):
        click.echo(f"{i}. {action}")
    choice = click.prompt("Select an option", type=click.IntRange(1, len(ACTIONS)))
    return ACTIONS[choice - 1]

@click.command()
def main():
    session = SessionLocal()

    while True:
        action = display_menu()

        if action == "Add Block":
            name = click.prompt("Enter block name")
            Block.create(session, name)

        elif action == "List Blocks":
            blocks = Block.get_all(session)
            for b in blocks:
                click.echo(f"[{b.id}] Block {b.name}")

        elif action == "Add Unit":
            number = click.prompt("Enter unit number (e.g., 204)")
            block_id = click.prompt("Enter block ID", type=int)
            Unit.create(session, number, block_id)

        elif action == "List Vacant Units":
            units = Unit.get_vacant_units(session)
            click.echo("-----VACANT UNITS-----")
            if units:
                for u in units:
                    click.echo(f"[{u.id}]Unit {u.number} in Block {u.block.name}")
            else:
                click.echo("All units are currently occupied.")
            click.echo("--------------------")

        elif action == "Add Tenant":
            name = click.prompt("Tenant name")
            phone = click.prompt("Phone number")
            email = click.prompt("Email")
            unit_id = click.prompt("Unit ID to assign tenant to", type=int)
            Tenant.create(session, name, phone, email, unit_id)

        elif action == "List Tenants":
            tenants = Tenant.get_all(session)
            if tenants:
                for t in tenants:
                    click.echo(f"{t.id}. {t.name} – Unit {t.unit.number} (Block {t.unit.block.name})")
            else:
                click.echo("No tenants found.")

        elif action == "Add Payment":
            tenant_id = click.prompt("Tenant ID", type=int)
            amount = click.prompt("Amount paid", type=float)
            Payment.create(session, tenant_id, amount)

        elif action == "List Payments":
             click.echo("\nView payments by:")
             click.echo("1. All Payments")
             click.echo("2. By Tenant ID")
             click.echo("3. By Payment ID")
         
             option = click.prompt("Choose an option", type=click.IntRange(1, 3))
         
             if option == 1:
                 payments = Payment.get_all(session)
                 if payments:
                     for p in payments:
                         tenant = p.tenant
                         click.echo(f"{p.id}: {tenant.name} – {p.amount} KES on {p.date_paid}")
                 else:
                     click.echo("No payments found.")
         
             elif option == 2:
                 tenant_id = click.prompt("Tenant ID", type=int)
                 payments = Payment.get_by_tenant(session, tenant_id)
                 tenant = Tenant.get_by_id(session, tenant_id)
                 if not tenant:
                     click.echo("Tenant not found.")
                 else:
                     click.echo(f"\nPayments for {tenant.name}:\n")
                     payments = Payment.get_by_tenant(session, tenant_id)
                     if payments:
                         for p in payments:
                             click.echo(f"{p.id}: {p.amount} KES on {p.date_paid}")
                     else:
                         click.echo("No payments found for this tenant.")
         
             elif option == 3:
                 payment_id = click.prompt("Payment ID", type=int)
                 payment = Payment.get_by_id(session, payment_id)
                 if payment:
                     tenant = payment.tenant
                     click.echo(f"{payment.id}: {tenant.name} – {payment.amount} KES on {payment.date_paid}")
                 else:
                     click.echo("Payment not found.")
                
        elif action == "Vacate Tenant":
            tenant_id = click.prompt("Enter the Tenant ID to vacate", type=int)
            Tenant.vacate(session, tenant_id)

        elif action == "Check Pending Payments":
             month = click.prompt("Enter month (1-12)", type=int)
             year = click.prompt("Enter year", type=int)
             defaulters = Tenant.get_defaulters(session, month, year)

             if defaulters:
                 click.echo(f"\nTenants with pending payments for {month}/{year}:")
                 for t in defaulters:
                     click.echo(f"{t.id}. {t.name} - Unit {t.unit.number} (Block {t.unit.block.name})")
             else:
                 click.echo(f"No pending payments for {month}/{year}.")


        elif action == "Exit":
            click.echo("Goodbye.")
            break

    session.close()

if __name__ == "__main__":
    main()