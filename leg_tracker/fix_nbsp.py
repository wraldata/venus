from billcatcher.models import Lawmaker

p = Lawmaker.objects.get(pk=17936)

p.name = 'Jay Chaudhuri'

p.save() 