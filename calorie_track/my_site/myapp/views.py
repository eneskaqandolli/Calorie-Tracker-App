from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Food, Consume

# Create your views here.
def index(request):
    if request.method == "POST":
        food_consumed = request.POST["foods"]
        consume = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=consume)
        consume.save()
        foods = Food.objects.all()
        return redirect("food_list")

    consumed_foods = Consume.objects.filter(user=request.user)
    foods = Food.objects.all()
    
    calorie_goal = 2400
    
    total_carbs = round(sum(food.food_consumed.carbs for food in consumed_foods),2)
    total_protein = round(sum(food.food_consumed.protein for food in consumed_foods),2)
    total_fats = round(sum(food.food_consumed.fats for food in consumed_foods),2)
    total_calories = round(sum(food.food_consumed.calories for food in consumed_foods),2)
    
    if calorie_goal > 0:
        progress_percentage = round(min(100, (total_calories / calorie_goal) * 100))
    else:
        progress_percentage = 0
    
    context = {
        "foods": foods, 
        "consumed_foods": consumed_foods,
        "total_carbs": total_carbs,
        "total_protein": total_protein,
        "total_fats": total_fats,
        "total_calories": total_calories,
        "progress": progress_percentage,
    }
    
    return render(request, "myapp/index.html", context)

def delete(request, id):
    deleted_consume = get_object_or_404(Consume, id=id)
    deleted_consume.delete()
    messages.success(request, 'Item deleted successfully')
    return redirect("/foods")

