from..models import Implemento

class ImplementoFactory:
    def crear_implemento(self, itype, worker, description):
        
        implemento = Implemento(
            itype = itype,
            worker = worker,
            description = description
        )
        implemento.save()
        return implemento