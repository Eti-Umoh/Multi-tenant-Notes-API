from server.main_utils import to_ui_readable_datetime_format
from server.investments.utils import (get_disbursements_by_investor, investor_get_investments,
                                      get_project_by_id)
from server.roles.utils import get_role_by_id


async def user_serializer(user, db):
    disbursements = await get_disbursements_by_investor(
        user.id, "upcoming", db)
    
    # Find the next earning amount from the upcoming disbursements
    next_earning = 0
    next_disbursement = None
    if disbursements:
        # Sort upcoming disbursements by date and get the earliest one
        next_disbursement = min(disbursements, key=lambda d: d.date)
        next_earning = round(next_disbursement.amount, 2)

    amount_invested = 0
    projects = []
    investments = await investor_get_investments(user.id, db=db)
    if investments:
        for investment in investments:
            project = await get_project_by_id(investment.project, db)
            projects.append(project)
            amount_invested += investment.amount
    projects_count = len(projects) 

    role = await get_role_by_id(user.role, db)
    role_title = None
    if role:
        role_title = role.title

    items = {
        "id": user.id,
        "user_id": user.user_id,
        "image": user.image if user.image else "",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email_address": user.email_address,
        "phone_number": user.phone,
        "user_type": str(user.user_type.name),
        "gender": user.gender,
        "initial_login": user.initial_login,
        "email_verified": user.email_verified,
        "edit_bank_info": user.edit_bank_info,
        "status": user.status,
        "identification": user.identification,
        "identification_type": user.identification_type,
        "bank_name": user.bank_name,
        "account_number": user.account_number,
        "account_name": user.account_name,
        "next_disbursement": next_earning,
        "disbursement_date": to_ui_readable_datetime_format(next_disbursement.date) if next_disbursement else "",
        "total_capital_invested": amount_invested,
        "active_projects": projects_count,
        "vip": user.vip,
        "password_changed": user.password_changed,
        "referral_code": user.referral_code,
        "role": role_title,
        "commission": user.commission,
        "created_at": to_ui_readable_datetime_format(user.created_at),
        "updated_at": to_ui_readable_datetime_format(user.updated_at) if user.updated_at else ""
    }
    return items