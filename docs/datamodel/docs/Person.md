
# Class: Person


a person,living or dead

URI: [TEMP:Person](http://example.org/TEMP/Person)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[MedicalEvent]<has%20medical%20history%200..*-++[Person&#124;id:string;name:string;age:decimal%20%3F;gender:decimal%20%3F],[MedicalEvent])](https://yuml.me/diagram/nofunky;dir:TB/class/[MedicalEvent]<has%20medical%20history%200..*-++[Person&#124;id:string;name:string;age:decimal%20%3F;gender:decimal%20%3F],[MedicalEvent])

## Referenced by Class


## Attributes


### Own

 * [Person➞id](Person_id.md)  <sub>1..1</sub>
     * Description: identifier for a person
     * Range: [String](types/String.md)
 * [Person➞name](Person_name.md)  <sub>1..1</sub>
     * Description: full name
     * Range: [String](types/String.md)
 * [Person➞age](Person_age.md)  <sub>0..1</sub>
     * Description: age in years
     * Range: [Decimal](types/Decimal.md)
 * [Person➞gender](Person_gender.md)  <sub>0..1</sub>
     * Description: age in years
     * Range: [Decimal](types/Decimal.md)
 * [Person➞has medical history](Person_has_medical_history.md)  <sub>0..\*</sub>
     * Description: medical history
     * Range: [MedicalEvent](MedicalEvent.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | sdo:Person |
|  | | wikidata:Q215627 |

