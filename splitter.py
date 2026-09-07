from typing import Dict, List
from schemas import BillData

def calculate_split(
    bill: BillData, 
    assignments: Dict[int, List[str]], 
    friends: List[str]
) -> Dict[str, Dict]:
    # Track raw item subtotal consumed by each person
    friend_subtotals = {f: 0.0 for f in friends}
    
    # 1. Distribute raw item costs among assigned people
    for idx, item in enumerate(bill.items):
        assigned_to = assignments.get(idx, [])
        if not assigned_to:
            continue
        split_cost = float(item.price) / len(assigned_to)
        for friend in assigned_to:
            friend_subtotals[friend] += split_cost

    total_consumed_subtotal = sum(friend_subtotals.values())
    net_extra_charges = float(bill.gst_tax) + float(bill.service_charge) - float(bill.discount)
    
    results = {}
    for friend in friends:
        raw_share = friend_subtotals[friend]
        # Proportional ratio based on what they ate vs total food eaten
        ratio = (raw_share / total_consumed_subtotal) if total_consumed_subtotal > 0 else 0
        proportional_extra = net_extra_charges * ratio
        total_owed = raw_share + proportional_extra

        results[friend] = {
            "subtotal": round(raw_share, 2),
            "proportional_fees": round(proportional_extra, 2),
            "total": round(total_owed, 2)
        }
        
    return results