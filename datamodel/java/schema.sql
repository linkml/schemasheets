

CREATE TABLE "ForProfit" (
	name TEXT NOT NULL, 
	PRIMARY KEY (name)
);

CREATE TABLE "NonProfit" (
	name TEXT NOT NULL, 
	PRIMARY KEY (name)
);

CREATE TABLE "Organization" (
	name TEXT NOT NULL, 
	PRIMARY KEY (name)
);

CREATE TABLE "Person" (
	id TEXT NOT NULL, 
	name TEXT NOT NULL, 
	age TEXT, 
	gender TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "MedicalEvent" (
	"Person_id" TEXT, 
	PRIMARY KEY ("Person_id"), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
