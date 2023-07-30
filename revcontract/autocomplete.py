from .models import BCBSGS
from django.views import View
from .models import BCBSGS
from django.http import JsonResponse
from django.db.models import Q


def create_word_regex(input_string):
    words = input_string.split()
    regex_pattern = r'({})'.format("|".join(words))
    return regex_pattern
class BCBSGSAutocomplete(View):

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        
        try:    
            words = q.split()
            query = Q(name__icontains=words[0]) | Q(code__icontains=words[0])
            for word in words:
                query &= Q(name__icontains=word) | Q(code__icontains=word)        
            codes = BCBSGS.objects.filter(query)
        except:
            codes = BCBSGS.objects.filter(Q(name__icontains=q) | Q(code__icontains=q))
        
        results = []

        for code in codes:
            results.append({
                'id': code.pk,
                'text': f'{code.code} - {code.name}',
            })
        
        return JsonResponse({'items': results})