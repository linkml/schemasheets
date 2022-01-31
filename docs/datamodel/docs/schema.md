
# TEMP schema





### Classes

 * [Event](Event.md) - grouping class for events
     * [MedicalEvent](MedicalEvent.md) - a medical encounter
 * [Organization](Organization.md)
     * [ForProfit](ForProfit.md)
     * [NonProfit](NonProfit.md)
 * [Person](Person.md) - a person,living or dead

### Mixins


### Slots

 * [age](age.md)
     * [Person➞age](Person_age.md) - age in years
 * [description](description.md) - a textual description
 * [gender](gender.md)
     * [Person➞gender](Person_gender.md) - age in years
 * [has medical history](has_medical_history.md)
     * [Person➞has medical history](Person_has_medical_history.md) - medical history
 * [id](id.md) - any identifier
     * [Person➞id](Person_id.md) - identifier for a person
 * [name](name.md)
     * [Organization➞name](Organization_name.md) - full name
     * [Person➞name](Person_name.md) - full name

### Enums


### Subsets

 * [A](A.md)
 * [B](B.md)

### Types


#### Built in

 * **Bool**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
