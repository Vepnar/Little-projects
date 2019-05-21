// Author: Arjan de Haan (Vepnar)
// My first go project
// I don't like Hello worlds so I made this

package main

import "fmt"

/*
	All Si prefixes above 1000
	See: https://en.wikipedia.org/wiki/Metric_prefix
*/
var SI_PREFIXES = [9]byte{' ', 'K', 'M', 'G','T','P','E','Z','Y'}

/*
	Read integer input
	Source: https://stackoverflow.com/questions/3751429/reading-an-integer-from-standard-input	
*/
func input_mass() int {
	var i int
	fmt.Print("Insert mass in kg > ")
	fmt.Scan(&i)
	return i;
}

func format_si(value int64, si string) string {
	current := value

	for i := 0; i < 10; i++ {

		if current < 999 {
			prefix := SI_PREFIXES[i]
			if prefix == ' '{
				return fmt.Sprintf("\t%d%s", value, si)
			}
			return fmt.Sprintf("\t%d%c%s", current, prefix, si)

		}else {
			current = current / 1000
		}
	}
	return fmt.Sprintf("\t%d%s", value, si)

}

/* 
	Convert kg to joule
	See: https://en.wikipedia.org/wiki/Mass%E2%80%93energy_equivalence
*/
func convert_kg_to_joule(kg int) int64 {
	var kg64 =  int64(kg);
	return kg64 * 89875517873681764;
}

/*
	Convert joule to large calories
	See: https://www.rapidtables.com/convert/energy/how-joule-to-cal.html
*/
func convert_calories(joule int64) string {
	cal := joule / 4
	return format_si(cal,"Cal")
}

/* 
	Convert joule to British terminal unit
	See: https://en.wikipedia.org/wiki/British_thermal_unit
*/
func convert_btu(joule int64) string {
	btu := joule / 1060
	return format_si(btu, " BTU") 
}

/*
	Convert joule to Watt hours
	See: https://en.wikipedia.org/wiki/Kilowatt_hour
*/
func convert_watthour(joule int64) string {
	wh := joule / 3600000
	return format_si(wh,"Wh")
}

/*
	Convert joule to tnt equivalent
	See: https://en.wikipedia.org/wiki/TNT_equivalent
*/
func convert_tnt(joule int64) string {
	tnt := joule / 4184
	return format_si(tnt, " of TNT")
}

/*
	Convert joule to Tsar bomba
	See: https://en.wikipedia.org/wiki/Tsar_Bomba
*/
func convert_tsar(joule int64) string {
	tsar := int64(210000000000000000)
	if joule > tsar {
		tsar := joule / tsar
		return format_si(tsar, " Tsar bomba")
	}
	return "\t0 Tsar bomba"
}

/*
	Convert joule to quad
	See: https://en.wikipedia.org/wiki/Quad_(unit)
*/
func convert_quad(joule int64) string {
	quad := int64(1055000000000000000)
	if joule > quad {
		quad := joule / quad
		return format_si(quad, " Quads")
	}
	return "\t0 quads"

}

func main() {
	kg := input_mass();
	j := convert_kg_to_joule(kg);

	fmt.Println(format_si(j,"J")) // Joule
	fmt.Println(convert_watthour(j)) // Watt hour
	fmt.Println(convert_calories(j)) // Calories
	fmt.Println(convert_btu(j)) // British terminal unit
	fmt.Println(convert_tnt(j)) // Convert tnt
	fmt.Println(convert_tsar(j)) // Convert Tsar bomba
	fmt.Println(convert_quad(j)) // Convert to quads
	
}
