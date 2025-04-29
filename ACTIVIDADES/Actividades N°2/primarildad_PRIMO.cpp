	#include <cmath>
	
	bool es_primo(int val) {
	    if (val < 2)
        return false;
	    if (val == 2)
	        return true;
	    if (val % 2 == 0)
	        return false;
	
	    // Verificar divisores impares hasta la raíz cuadrada de val
	    for (int i = 3; i <= sqrt(val); i += 2) {
	        if (val % i == 0)
	            return false;
	    }
	    return true;
	}

